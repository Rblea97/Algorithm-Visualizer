import tkinter as tk
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import COLORS, LEGEND_PANEL_WIDTH, LEGEND_ITEMS


class LegendPanel:
    """
    Right panel showing color legend and completion messages.

    Displays what each bar color represents and provides space
    for celebration messages when sorting completes.
    """

    def __init__(self, parent: tk.Widget):
        """
        Initialize legend panel.

        Args:
            parent: Parent widget to contain this panel
        """
        self.parent = parent

        # Create main frame
        self.frame = tk.Frame(parent, bg=COLORS["PANEL_BG"], width=LEGEND_PANEL_WIDTH)
        self.frame.pack(fill="both", expand=True)
        self.frame.pack_propagate(False)  # Maintain fixed width

        # Create widgets
        self._create_widgets()
        self._setup_layout()

    def _create_widgets(self):
        """Create legend widgets."""

        # Legend title
        self.title_label = tk.Label(
            self.frame,
            text="Legend",
            bg=COLORS["PANEL_BG"],
            fg=COLORS["TEXT"],
            font=("Arial", 10, "bold"),
        )

        # Color legend items
        self.legend_items = []
        for label, color in LEGEND_ITEMS:
            # Create frame for each legend item
            item_frame = tk.Frame(self.frame, bg=COLORS["PANEL_BG"])

            # Color square
            color_canvas = tk.Canvas(
                item_frame,
                width=20,
                height=15,
                bg=color,
                highlightthickness=1,
                highlightbackground=COLORS["TEXT"],
            )

            # Label
            label_widget = tk.Label(
                item_frame,
                text=label,
                bg=COLORS["PANEL_BG"],
                fg=COLORS["TEXT"],
                font=("Arial", 8),
            )

            # Pack within item frame
            color_canvas.pack(side="left", padx=(0, 5))
            label_widget.pack(side="left", fill="x", expand=True)

            self.legend_items.append((item_frame, color_canvas, label_widget))

        # Completion message area
        self.completion_frame = tk.Frame(self.frame, bg=COLORS["PANEL_BG"])

        self.completion_label = tk.Label(
            self.completion_frame,
            text="",
            bg=COLORS["PANEL_BG"],
            fg=COLORS["SUCCESS"],
            font=("Arial", 12, "bold"),
            wraplength=LEGEND_PANEL_WIDTH - 20,
            justify="center",
        )

        # Statistics display
        self.stats_frame = tk.Frame(self.frame, bg=COLORS["PANEL_BG"])

        self.stats_label = tk.Label(
            self.stats_frame,
            text="",
            bg=COLORS["PANEL_BG"],
            fg=COLORS["TEXT"],
            font=("Arial", 8),
            wraplength=LEGEND_PANEL_WIDTH - 20,
            justify="left",
        )

    def _setup_layout(self):
        """Arrange widgets in the legend panel."""
        y = 20

        # Title
        self.title_label.place(x=10, y=y)
        y += 30

        # Legend items
        for item_frame, _, _ in self.legend_items:
            item_frame.place(x=10, y=y, width=LEGEND_PANEL_WIDTH - 20, height=20)
            y += 25

        # Add some spacing
        y += 20

        # Completion message (positioned for visibility)
        self.completion_frame.place(x=10, y=y, width=LEGEND_PANEL_WIDTH - 20, height=60)
        self.completion_label.pack(expand=True)
        y += 70

        # Statistics
        self.stats_frame.place(x=10, y=y, width=LEGEND_PANEL_WIDTH - 20, height=100)
        self.stats_label.pack(fill="both", expand=True)

    def show_completion_message(self, message: str = "Sort Complete!"):
        """
        Display completion message.

        Args:
            message: Message to display
        """
        self.completion_label.config(text=message)

        # Flash the message by temporarily changing color
        self.completion_label.config(fg=COLORS["SUCCESS"])
        self.frame.after(
            100, lambda: self.completion_label.config(fg=COLORS["SUCCESS"])
        )

    def show_statistics(self, stats: dict):
        """
        Display sorting statistics.

        Args:
            stats: Dictionary containing statistics like steps, comparisons, swaps
        """
        stats_text = ""

        if "total_steps" in stats:
            stats_text += f"Steps: {stats['total_steps']}\n"
        if "comparisons" in stats:
            stats_text += f"Comparisons: {stats['comparisons']}\n"
        if "swaps" in stats:
            stats_text += f"Swaps: {stats['swaps']}\n"
        if "time_taken" in stats:
            stats_text += f"Time: {stats['time_taken']:.2f}s\n"

        self.stats_label.config(text=stats_text)

    def clear_messages(self):
        """Clear completion message and statistics."""
        self.completion_label.config(text="")
        self.stats_label.config(text="")

    def flash_completion(self):
        """Flash the completion message for celebratory effect."""
        original_bg = self.completion_label.cget("bg")
        flash_color = COLORS["SUCCESS"]

        def flash_sequence(step=0):
            if step < 6:  # Flash 3 times
                color = flash_color if step % 2 == 0 else original_bg
                self.completion_frame.config(bg=color)
                self.frame.after(200, lambda: flash_sequence(step + 1))
            else:
                self.completion_frame.config(bg=original_bg)

        flash_sequence()

    def get_widget(self) -> tk.Frame:
        """Get the legend panel frame."""
        return self.frame
