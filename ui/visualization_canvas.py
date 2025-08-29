import tkinter as tk
from typing import List, Dict, Any, Optional, Set
from utils import (
    COLORS,
    VISUALIZATION_CANVAS_WIDTH,
    CANVAS_HEIGHT,
    CANVAS_PADDING,
    BAR_SPACING,
    BAR_TEXT_OFFSET,
)


class VisualizationCanvas:
    """
    Central canvas for displaying animated bar chart visualization of sorting algorithms.

    Handles smooth bar animations, color transitions, and value labels with
    interpolation for 60fps performance.
    """

    def __init__(self, parent: tk.Widget):
        """
        Initialize visualization canvas.

        Args:
            parent: Parent widget to contain this canvas
        """
        self.parent = parent

        # Create canvas
        self.canvas = tk.Canvas(
            parent,
            width=VISUALIZATION_CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            bg=COLORS["BACKGROUND"],
            highlightthickness=0,
        )

        # State management
        self.array: List[int] = []
        self.bar_states: Dict[int, str] = (
            {}
        )  # index -> state ('default', 'comparing', etc.)
        self.bar_rects: List[Optional[int]] = []  # Canvas rectangle IDs
        self.bar_texts: List[Optional[int]] = []  # Canvas text IDs

        # Animation state for smooth transitions
        self.animation_data: Dict[int, Dict[str, Any]] = {}  # index -> animation info
        self.comparing_indices: Set[int] = set()
        self.swapping_indices: Set[int] = set()
        self.sorted_indices: Set[int] = set()

        # Layout calculations
        self.bar_width = 0
        self.max_bar_height = 0
        self.base_y = 0

    def set_array(self, array: List[int]):
        """
        Set the array to visualize and calculate layout.

        Args:
            array: List of integers to visualize
        """
        self.array = array.copy()
        self.bar_states = {i: "default" for i in range(len(array))}

        # Clear animation state
        self.animation_data.clear()
        self.comparing_indices.clear()
        self.swapping_indices.clear()
        self.sorted_indices.clear()

        # Calculate layout
        self._calculate_layout()

        # Draw initial bars
        self.draw_bars()

    def _calculate_layout(self):
        """Calculate bar dimensions and positions based on array size."""
        if not self.array:
            return

        array_size = len(self.array)
        available_width = VISUALIZATION_CANVAS_WIDTH - (2 * CANVAS_PADDING)
        total_spacing = BAR_SPACING * (array_size - 1)

        # Calculate bar width
        self.bar_width = max(10, (available_width - total_spacing) // array_size)

        # Calculate maximum bar height (leave room for text)
        self.max_bar_height = CANVAS_HEIGHT - (2 * CANVAS_PADDING) - 20
        self.base_y = CANVAS_HEIGHT - CANVAS_PADDING

    def _get_bar_x(self, index: int) -> int:
        """Get X position for bar at given index."""
        return CANVAS_PADDING + index * (self.bar_width + BAR_SPACING)

    def _get_bar_height(self, value: int) -> int:
        """Get height for bar with given value."""
        if not self.array:
            return 0
        max_value = max(self.array)
        min_value = min(self.array)
        value_range = max_value - min_value

        if value_range == 0:
            return self.max_bar_height // 2

        normalized = (value - min_value) / value_range
        return max(10, int(normalized * self.max_bar_height))

    def _get_bar_color(self, index: int) -> str:
        """Get current color for bar at given index."""
        if index in self.sorted_indices:
            return COLORS["SORTED"]
        elif index in self.swapping_indices:
            return COLORS["SWAPPING"]
        elif index in self.comparing_indices:
            return COLORS["COMPARING"]
        else:
            return COLORS["DEFAULT"]

    def draw_bars(self):
        """Draw all bars on the canvas."""
        # Clear canvas
        self.canvas.delete("all")

        if not self.array:
            return

        # Reset ID lists
        self.bar_rects = [None] * len(self.array)
        self.bar_texts = [None] * len(self.array)

        # Draw each bar
        for i, value in enumerate(self.array):
            self._draw_single_bar(i, value)

    def _draw_single_bar(self, index: int, value: int, x_offset: float = 0):
        """
        Draw a single bar with optional position offset for animations.

        Args:
            index: Bar index
            value: Bar value
            x_offset: Additional X offset for animation
        """
        x = self._get_bar_x(index) + x_offset
        height = self._get_bar_height(value)
        y = self.base_y - height
        color = self._get_bar_color(index)

        # Draw rectangle
        rect_id = self.canvas.create_rectangle(
            x,
            y,
            x + self.bar_width,
            self.base_y,
            fill=color,
            outline=COLORS["TEXT"],
            width=1,
        )

        # Draw value text
        text_x = x + self.bar_width // 2
        text_y = y - BAR_TEXT_OFFSET
        text_id = self.canvas.create_text(
            text_x,
            text_y,
            text=str(value),
            fill=COLORS["TEXT"],
            font=("Arial", 8),
            anchor="s",
        )

        # Store IDs
        if index < len(self.bar_rects):
            self.bar_rects[index] = rect_id
            self.bar_texts[index] = text_id

    def update_animation(
        self,
        action: str,
        indices: List[int],
        description: str,
        animation_data: Optional[Dict[str, Any]] = None,
    ):
        """
        Update visualization based on animation step.

        Args:
            action: Animation action type
            indices: Indices involved in the action
            description: Step description
            animation_data: Animation interpolation data
        """
        if not animation_data:
            animation_data = {"progress": 1.0, "is_final_frame": True}

        progress = animation_data.get("progress", 1.0)
        is_final_frame = animation_data.get("is_final_frame", True)

        # Check if algorithm provides updated array state
        if "array_state" in animation_data and is_final_frame:
            # Update our array to match the algorithm's current state
            self.array = animation_data["array_state"].copy()

        # Handle different action types
        if action == "compare":
            self._handle_compare(indices, progress, is_final_frame)
        elif action == "swap":
            self._handle_swap(indices, progress, is_final_frame)
        elif action in ["mark_sorted", "sorted"]:
            self._handle_mark_sorted(indices)
        elif action in ["highlight_pivot", "highlight_current", "highlight_min"]:
            self._handle_highlight(indices, progress, is_final_frame)
        elif action == "reset":
            self._handle_reset()
        elif action == "array_update":
            # Handle array state update from algorithms
            self._handle_array_update(indices, progress, is_final_frame, description)
        elif action in ["divide", "merge_start", "place", "insert", "shift"]:
            # Handle merge sort specific actions
            self._handle_merge_actions(action, indices, progress, is_final_frame)

        # Redraw if this is a final frame or for certain actions
        if is_final_frame or action in ["reset", "mark_sorted", "array_update"]:
            self._redraw_affected_bars(indices)

    def _handle_compare(
        self, indices: List[int], progress: float, is_final_frame: bool
    ):
        """Handle comparison highlighting."""
        if is_final_frame:
            # Clear previous comparisons
            self.comparing_indices.clear()
            # Add current comparisons
            self.comparing_indices.update(indices)

    def _handle_swap(self, indices: List[int], progress: float, is_final_frame: bool):
        """Handle swapping animation with interpolation."""
        if len(indices) != 2:
            return

        idx1, idx2 = indices

        if progress == 0.0:
            # Start of swap - mark as swapping
            self.swapping_indices.update(indices)
            self.comparing_indices.discard(idx1)
            self.comparing_indices.discard(idx2)
        elif is_final_frame:
            # Complete swap - actually swap values and clear swap state
            self.array[idx1], self.array[idx2] = self.array[idx2], self.array[idx1]
            self.swapping_indices.discard(idx1)
            self.swapping_indices.discard(idx2)
        else:
            # Mid-swap - animate positions
            self._animate_swap_positions(idx1, idx2, progress)

    def _handle_mark_sorted(self, indices: List[int]):
        """Handle marking elements as sorted."""
        self.sorted_indices.update(indices)
        # Remove from other states
        for idx in indices:
            self.comparing_indices.discard(idx)
            self.swapping_indices.discard(idx)

    def _handle_highlight(
        self, indices: List[int], progress: float, is_final_frame: bool
    ):
        """Handle general highlighting (pivot, current element, etc.)."""
        if is_final_frame:
            self.comparing_indices.update(indices)

    def _handle_array_update(
        self,
        indices: List[int],
        progress: float,
        is_final_frame: bool,
        description: str,
    ):
        """Handle array state updates from algorithms."""
        if is_final_frame and "Array updated:" in description:
            # Extract the new array state from the description
            try:
                # Parse the array from the description string
                import ast

                array_str = description.split("Array updated: ")[1]
                new_array = ast.literal_eval(array_str)
                if isinstance(new_array, list) and len(new_array) == len(self.array):
                    self.array = new_array.copy()
            except (ValueError, IndexError, SyntaxError):
                # If parsing fails, ignore the update
                pass

    def _handle_reset(self):
        """Reset all visual states."""
        self.comparing_indices.clear()
        self.swapping_indices.clear()
        self.sorted_indices.clear()
        self.animation_data.clear()
        self.draw_bars()

    def _handle_merge_actions(
        self, action: str, indices: List[int], progress: float, is_final_frame: bool
    ):
        """Handle merge sort and insertion sort specific actions."""
        if action == "divide":
            # Highlight the section being divided
            if is_final_frame and len(indices) >= 2:
                self.comparing_indices.update(range(indices[0], indices[-1] + 1))
        elif action == "merge_start":
            # Highlight sections being merged
            if is_final_frame and len(indices) >= 3:
                left, _mid, right = indices[0], indices[1], indices[2]
                self.comparing_indices.update(range(left, right + 1))
        elif action == "place":
            # Merge sort: place element at specific position
            # This needs special handling as merge sort reconstructs the array
            if is_final_frame:
                self.comparing_indices.update(indices)
        elif action == "insert":
            # Insertion sort: insert element at specific position
            if is_final_frame:
                self.comparing_indices.update(indices)
        elif action == "shift":
            # Insertion sort: shift elements to make room
            if is_final_frame:
                self.comparing_indices.update(indices)

    def _animate_swap_positions(self, idx1: int, idx2: int, progress: float):
        """
        Animate swapping positions with smooth interpolation.

        Args:
            idx1: First index
            idx2: Second index
            progress: Animation progress (0.0 to 1.0)
        """
        # Calculate position offsets
        x1 = self._get_bar_x(idx1)
        x2 = self._get_bar_x(idx2)

        # Interpolate positions
        offset1 = (x2 - x1) * progress
        offset2 = (x1 - x2) * progress

        # Clear and redraw with offsets
        if self.bar_rects[idx1]:
            self.canvas.delete(self.bar_rects[idx1])
        if self.bar_texts[idx1]:
            self.canvas.delete(self.bar_texts[idx1])
        if self.bar_rects[idx2]:
            self.canvas.delete(self.bar_rects[idx2])
        if self.bar_texts[idx2]:
            self.canvas.delete(self.bar_texts[idx2])

        # Draw bars at interpolated positions
        self._draw_single_bar(idx1, self.array[idx1], offset1)
        self._draw_single_bar(idx2, self.array[idx2], offset2)

    def _redraw_affected_bars(self, indices: List[int]):
        """Redraw only the bars that were affected by the last action."""
        if not indices:
            # If no specific indices, redraw all
            self.draw_bars()
            return

        for idx in indices:
            if 0 <= idx < len(self.array):
                # Delete old bar
                if idx < len(self.bar_rects) and self.bar_rects[idx]:
                    self.canvas.delete(self.bar_rects[idx])
                if idx < len(self.bar_texts) and self.bar_texts[idx]:
                    self.canvas.delete(self.bar_texts[idx])

                # Draw new bar
                self._draw_single_bar(idx, self.array[idx])

    def highlight_completion(self):
        """Special animation for sorting completion."""
        # Flash all bars green
        self.sorted_indices = set(range(len(self.array)))
        self.comparing_indices.clear()
        self.swapping_indices.clear()
        self.draw_bars()

        # Could add a pulsing effect here in future versions

    def get_widget(self) -> tk.Canvas:
        """Get the canvas widget."""
        return self.canvas
