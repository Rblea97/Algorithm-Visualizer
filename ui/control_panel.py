import tkinter as tk
from tkinter import ttk
import random
from typing import List, Callable, Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import (
    COLORS,
    CONTROL_PANEL_WIDTH,
    CONTROL_Y_START,
    ARRAY_SIZE_DEFAULT,
    ARRAY_SIZE_MIN,
    ARRAY_SIZE_MAX,
    ANIMATION_SPEED_DEFAULT,
    ANIMATION_SPEED_MIN,
    ANIMATION_SPEED_MAX,
    VALUE_MIN,
    BUTTON_SYMBOLS,
    ALGORITHM_INFO,
    InputValidator,
)


class ControlPanel:
    """
    Left panel containing all user controls for the sorting visualizer.

    Includes algorithm selection, array controls, playback controls,
    speed control, and progress display.
    """

    def __init__(self, parent: tk.Widget):
        """
        Initialize control panel.

        Args:
            parent: Parent widget to contain this panel
        """
        self.parent = parent

        # Create main frame
        self.frame = tk.Frame(parent, bg=COLORS["PANEL_BG"], width=CONTROL_PANEL_WIDTH)
        self.frame.pack(fill="both", expand=True)
        self.frame.pack_propagate(False)  # Maintain fixed width

        # Callbacks
        self.on_algorithm_change: Optional[Callable[[str], None]] = None
        self.on_array_change: Optional[Callable[[List[int]], None]] = None
        self.on_play: Optional[Callable[[], None]] = None
        self.on_pause: Optional[Callable[[], None]] = None
        self.on_reset: Optional[Callable[[], None]] = None
        self.on_speed_change: Optional[Callable[[float], None]] = None

        # State
        self.current_array: List[int] = []
        self.is_playing = False

        # Create UI elements
        self._create_widgets()
        self._setup_layout()

        # Initialize with random array
        self.generate_random_array()

    def _create_widgets(self):
        """Create all control widgets."""

        # Algorithm Selection
        self.algorithm_label = tk.Label(
            self.frame,
            text="Algorithm:",
            bg=COLORS["PANEL_BG"],
            fg=COLORS["TEXT"],
            font=("Arial", 10, "bold"),
        )

        self.algorithm_var = tk.StringVar()
        self.algorithm_combo = ttk.Combobox(
            self.frame,
            textvariable=self.algorithm_var,
            values=list(ALGORITHM_INFO.keys()),
            state="readonly",
            width=18,
        )
        self.algorithm_combo.bind("<<ComboboxSelected>>", self._on_algorithm_selected)

        # Algorithm Info Display
        self.info_frame = tk.Frame(self.frame, bg=COLORS["PANEL_BG"])
        self.complexity_label = tk.Label(
            self.info_frame,
            text="",
            bg=COLORS["PANEL_BG"],
            fg=COLORS["TEXT"],
            font=("Arial", 8),
            wraplength=200,
            justify="left",
        )

        # Array Size Control
        self.size_label = tk.Label(
            self.frame,
            text=f"Array Size: {ARRAY_SIZE_DEFAULT}",
            bg=COLORS["PANEL_BG"],
            fg=COLORS["TEXT"],
            font=("Arial", 9),
        )

        self.size_var = tk.IntVar(value=ARRAY_SIZE_DEFAULT)
        self.size_scale = tk.Scale(
            self.frame,
            from_=ARRAY_SIZE_MIN,
            to=ARRAY_SIZE_MAX,
            orient="horizontal",
            variable=self.size_var,
            bg=COLORS["PANEL_BG"],
            fg=COLORS["TEXT"],
            highlightbackground=COLORS["PANEL_BG"],
            troughcolor=COLORS["BACKGROUND"],
            command=self._on_size_change,
        )

        # Data Input Options
        self.random_button = tk.Button(
            self.frame,
            text="Generate Random",
            bg=COLORS["DEFAULT"],
            fg=COLORS["TEXT"],
            font=("Arial", 9),
            command=self.generate_random_array,
        )

        self.custom_label = tk.Label(
            self.frame,
            text="Custom Input:",
            bg=COLORS["PANEL_BG"],
            fg=COLORS["TEXT"],
            font=("Arial", 9),
        )

        self.custom_entry = tk.Entry(self.frame, width=20, font=("Arial", 9))
        self.custom_entry.bind("<Return>", self._on_custom_input)

        self.custom_button = tk.Button(
            self.frame,
            text="Apply",
            bg=COLORS["SUCCESS"],
            fg=COLORS["TEXT"],
            font=("Arial", 8),
            command=self._on_custom_input,
        )

        self.error_label = tk.Label(
            self.frame,
            text="",
            bg=COLORS["PANEL_BG"],
            fg=COLORS["ERROR"],
            font=("Arial", 8),
            wraplength=200,
            justify="left",
        )

        # Playback Controls
        self.controls_frame = tk.Frame(self.frame, bg=COLORS["PANEL_BG"])

        self.play_button = tk.Button(
            self.controls_frame,
            text=BUTTON_SYMBOLS["PLAY"],
            bg=COLORS["SUCCESS"],
            fg=COLORS["TEXT"],
            font=("Arial", 14),
            width=3,
            state="disabled",
            command=self._on_play_clicked,
        )

        self.pause_button = tk.Button(
            self.controls_frame,
            text=BUTTON_SYMBOLS["PAUSE"],
            bg=COLORS["ERROR"],
            fg=COLORS["TEXT"],
            font=("Arial", 14),
            width=3,
            state="disabled",
            command=self._on_pause_clicked,
        )

        self.reset_button = tk.Button(
            self.controls_frame,
            text=BUTTON_SYMBOLS["RESET"],
            bg=COLORS["BACKGROUND"],
            fg=COLORS["TEXT"],
            font=("Arial", 14),
            width=3,
            command=self._on_reset_clicked,
        )

        # Speed Control
        self.speed_label = tk.Label(
            self.frame,
            text=f"Speed: {ANIMATION_SPEED_DEFAULT:.1f}x",
            bg=COLORS["PANEL_BG"],
            fg=COLORS["TEXT"],
            font=("Arial", 9),
        )

        self.speed_var = tk.DoubleVar(value=ANIMATION_SPEED_DEFAULT)
        self.speed_scale = tk.Scale(
            self.frame,
            from_=ANIMATION_SPEED_MIN,
            to=ANIMATION_SPEED_MAX,
            orient="horizontal",
            variable=self.speed_var,
            resolution=0.1,
            bg=COLORS["PANEL_BG"],
            fg=COLORS["TEXT"],
            highlightbackground=COLORS["PANEL_BG"],
            troughcolor=COLORS["BACKGROUND"],
            command=self._on_speed_change,
        )

        # Progress Display
        self.progress_frame = tk.Frame(self.frame, bg=COLORS["PANEL_BG"])

        self.step_label = tk.Label(
            self.progress_frame,
            text="Step: 0 / 0",
            bg=COLORS["PANEL_BG"],
            fg=COLORS["TEXT"],
            font=("Arial", 9),
        )

        self.operation_label = tk.Label(
            self.frame,
            text="Ready to start",
            bg=COLORS["PANEL_BG"],
            fg=COLORS["TEXT"],
            font=("Arial", 8),
            wraplength=200,
            justify="left",
        )

    def _setup_layout(self):
        """Arrange all widgets in the control panel."""
        y = CONTROL_Y_START

        # Algorithm selection
        self.algorithm_label.place(x=10, y=y)
        y += 20
        self.algorithm_combo.place(x=10, y=y)
        y += 45  # More space after dropdown

        # Algorithm info
        self.info_frame.place(
            x=10, y=y, width=CONTROL_PANEL_WIDTH - 20, height=75
        )  # Increased height
        self.complexity_label.pack(
            fill="both", expand=True, padx=5, pady=5
        )  # Added padding
        y += 85  # More space after info

        # Array size
        self.size_label.place(x=10, y=y)
        y += 20
        self.size_scale.place(x=10, y=y, width=CONTROL_PANEL_WIDTH - 20)
        y += 40

        # Data input
        self.random_button.place(x=10, y=y, width=CONTROL_PANEL_WIDTH - 20)
        y += 35

        self.custom_label.place(x=10, y=y)
        y += 20
        self.custom_entry.place(x=10, y=y, width=140)
        self.custom_button.place(x=160, y=y, width=50)
        y += 35

        self.error_label.place(x=10, y=y, width=CONTROL_PANEL_WIDTH - 20, height=30)
        y += 40

        # Playback controls
        self.controls_frame.place(x=10, y=y, width=CONTROL_PANEL_WIDTH - 20, height=40)
        self.play_button.pack(side="left", padx=5)
        self.pause_button.pack(side="left", padx=5)
        self.reset_button.pack(side="left", padx=5)
        y += 50

        # Speed control
        self.speed_label.place(x=10, y=y)
        y += 20
        self.speed_scale.place(x=10, y=y, width=CONTROL_PANEL_WIDTH - 20)
        y += 40

        # Progress
        self.progress_frame.place(x=10, y=y, width=CONTROL_PANEL_WIDTH - 20, height=20)
        self.step_label.pack()
        y += 25

        self.operation_label.place(x=10, y=y, width=CONTROL_PANEL_WIDTH - 20, height=40)

    def _on_algorithm_selected(self, event=None):
        """Handle algorithm selection change."""
        algorithm = self.algorithm_var.get()
        if algorithm and algorithm in ALGORITHM_INFO:
            info = ALGORITHM_INFO[algorithm]
            complexity_text = (
                f"Time: {info['time_complexity']}\n"
                f"Space: {info['space_complexity']}\n\n"
                f"{info['description']}"
            )
            self.complexity_label.config(text=complexity_text)

            # Enable play button
            self.play_button.config(state="normal")

            # Clear error
            self.error_label.config(text="")

            # Notify callback
            if self.on_algorithm_change:
                self.on_algorithm_change(algorithm)

    def _on_size_change(self, value):
        """Handle array size change."""
        size = int(float(value))
        self.size_label.config(text=f"Array Size: {size}")

        # If currently using random array, regenerate
        if hasattr(self, "_last_was_random") and self._last_was_random:
            self.generate_random_array()

    def _on_custom_input(self, event=None):
        """Handle custom input submission."""
        input_text = self.custom_entry.get()
        is_valid, numbers, error = InputValidator.validate_input(input_text)

        if is_valid and numbers:
            self.current_array = numbers
            self._last_was_random = False
            self.error_label.config(text="")

            # Update size slider to match input
            self.size_var.set(len(numbers))
            self.size_label.config(text=f"Array Size: {len(numbers)}")

            # Notify callback
            if self.on_array_change:
                self.on_array_change(numbers)
        else:
            self.error_label.config(text=error or "Invalid input")

    def generate_random_array(self):
        """Generate a random array based on current size setting."""
        size = self.size_var.get()
        self.current_array = list(range(VALUE_MIN, VALUE_MIN + size))
        random.shuffle(self.current_array)
        self._last_was_random = True

        # Update custom entry to show generated array
        self.custom_entry.delete(0, "end")
        self.custom_entry.insert(0, InputValidator.format_input(self.current_array))

        # Clear error
        self.error_label.config(text="")

        # Notify callback
        if self.on_array_change:
            self.on_array_change(self.current_array)

    def _on_play_clicked(self):
        """Handle play button click."""
        self.is_playing = True
        self.play_button.config(state="disabled")
        self.pause_button.config(state="normal")
        self.algorithm_combo.config(state="disabled")

        if self.on_play:
            self.on_play()

    def _on_pause_clicked(self):
        """Handle pause button click."""
        self.is_playing = False
        self.play_button.config(state="normal")
        self.pause_button.config(state="disabled")

        if self.on_pause:
            self.on_pause()

    def _on_reset_clicked(self):
        """Handle reset button click."""
        self.is_playing = False
        self.play_button.config(
            state="normal" if self.algorithm_var.get() else "disabled"
        )
        self.pause_button.config(state="disabled")
        self.algorithm_combo.config(state="readonly")

        # Reset progress display
        self.update_progress(0, 0)
        self.update_operation("Ready to start")

        if self.on_reset:
            self.on_reset()

    def _on_speed_change(self, value):
        """Handle speed change."""
        speed = float(value)
        self.speed_label.config(text=f"Speed: {speed:.1f}x")

        if self.on_speed_change:
            self.on_speed_change(speed)

    def update_progress(self, current: int, total: int):
        """Update progress display."""
        self.step_label.config(text=f"Step: {current} / {total}")

    def update_operation(self, description: str):
        """Update current operation description."""
        self.operation_label.config(text=description)

    def set_algorithm_change_callback(self, callback: Callable[[str], None]):
        """Set callback for algorithm changes."""
        self.on_algorithm_change = callback

    def set_array_change_callback(self, callback: Callable[[List[int]], None]):
        """Set callback for array changes."""
        self.on_array_change = callback

    def set_playback_callbacks(
        self,
        play_callback: Callable[[], None],
        pause_callback: Callable[[], None],
        reset_callback: Callable[[], None],
    ):
        """Set playback control callbacks."""
        self.on_play = play_callback
        self.on_pause = pause_callback
        self.on_reset = reset_callback

    def set_speed_change_callback(self, callback: Callable[[float], None]):
        """Set callback for speed changes."""
        self.on_speed_change = callback

    def on_animation_complete(self):
        """Handle animation completion."""
        self.is_playing = False
        self.play_button.config(state="normal")
        self.pause_button.config(state="disabled")
        self.algorithm_combo.config(state="readonly")
        self.update_operation("Sort complete!")
