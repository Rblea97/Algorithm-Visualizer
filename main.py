"""
Sorting Algorithm Visualizer

A desktop application that visualizes sorting algorithms with smooth animations.
Built with Python tkinter for educational purposes.
"""

import tkinter as tk
from tkinter import messagebox
import sys
import time
from typing import Optional

from algorithms import ALGORITHMS
from ui import ControlPanel, VisualizationCanvas, LegendPanel
from utils import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    COLORS,
    CONTROL_PANEL_WIDTH,
    VISUALIZATION_CANVAS_WIDTH,
    LEGEND_PANEL_WIDTH,
    AnimationController,
)


class SortingVisualizerApp:
    """
    Main application class for the Sorting Algorithm Visualizer.

    Coordinates the three main UI panels and manages the animation controller
    to provide smooth, real-time visualization of sorting algorithms.
    """

    def __init__(self):
        """Initialize the sorting visualizer application."""
        self.root = tk.Tk()
        self.setup_window()

        # State management
        self.current_algorithm = None
        self.current_algorithm_instance = None
        self.current_array = []
        self.animation_start_time = 0

        # Create UI components
        self.create_panels()

        # Create animation controller
        self.animation_controller = AnimationController(
            self.root, self.on_animation_update
        )
        self.animation_controller.set_step_callback(self.on_step_change)
        self.animation_controller.set_completion_callback(self.on_animation_complete)

        # Connect panel callbacks
        self.setup_callbacks()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_window(self):
        """Configure the main application window."""
        self.root.title("Sorting Algorithm Visualizer")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        self.root.configure(bg=COLORS["BACKGROUND"])

        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (WINDOW_WIDTH // 2)
        y = (self.root.winfo_screenheight() // 2) - (WINDOW_HEIGHT // 2)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

    def create_panels(self):
        """Create and arrange the three main UI panels."""

        # Control Panel (left)
        control_frame = tk.Frame(
            self.root,
            width=CONTROL_PANEL_WIDTH,
            height=WINDOW_HEIGHT,
            bg=COLORS["PANEL_BG"],
        )
        control_frame.pack(side="left", fill="y")
        control_frame.pack_propagate(False)

        self.control_panel = ControlPanel(control_frame)

        # Visualization Canvas (center)
        canvas_frame = tk.Frame(
            self.root,
            width=VISUALIZATION_CANVAS_WIDTH,
            height=WINDOW_HEIGHT,
            bg=COLORS["BACKGROUND"],
        )
        canvas_frame.pack(side="left", fill="both")
        canvas_frame.pack_propagate(False)

        self.visualization_canvas = VisualizationCanvas(canvas_frame)
        self.visualization_canvas.get_widget().pack(expand=True)

        # Legend Panel (right)
        legend_frame = tk.Frame(
            self.root,
            width=LEGEND_PANEL_WIDTH,
            height=WINDOW_HEIGHT,
            bg=COLORS["PANEL_BG"],
        )
        legend_frame.pack(side="right", fill="y")
        legend_frame.pack_propagate(False)

        self.legend_panel = LegendPanel(legend_frame)

    def setup_callbacks(self):
        """Connect panel callbacks to application logic."""

        # Control panel callbacks
        self.control_panel.set_algorithm_change_callback(self.on_algorithm_change)
        self.control_panel.set_array_change_callback(self.on_array_change)
        self.control_panel.set_playback_callbacks(
            self.on_play, self.on_pause, self.on_reset
        )
        self.control_panel.set_speed_change_callback(self.on_speed_change)

    def on_algorithm_change(self, algorithm_name: str):
        """Handle algorithm selection change."""
        if algorithm_name in ALGORITHMS:
            self.current_algorithm = algorithm_name
            self.current_algorithm_instance = ALGORITHMS[algorithm_name]()

            # Clear previous visualization
            self.legend_panel.clear_messages()

            # Reset animation state
            self.animation_controller.reset()

            print(f"Selected algorithm: {algorithm_name}")

    def on_array_change(self, array: list):
        """Handle array data change."""
        self.current_array = array.copy()

        # Update visualization
        self.visualization_canvas.set_array(array)

        # Reset animation state
        self.animation_controller.reset()
        self.legend_panel.clear_messages()

        print(f"Array updated: {array}")

    def on_play(self):
        """Handle play button click."""
        if not self.current_algorithm_instance or not self.current_array:
            messagebox.showerror(
                "Error", "Please select an algorithm and provide array data"
            )
            return

        try:
            # Generate animation steps
            steps = self.current_algorithm_instance.get_steps(self.current_array)

            # Set up animation
            self.animation_controller.set_steps(steps)
            self.animation_start_time = time.time()

            # Clear previous messages
            self.legend_panel.clear_messages()

            # Start animation
            self.animation_controller.play()

            print(f"Started {self.current_algorithm} animation with {len(steps)} steps")

        except Exception as e:
            messagebox.showerror(
                "Animation Error", f"Failed to start animation: {str(e)}"
            )
            print(f"Animation error: {e}")

    def on_pause(self):
        """Handle pause button click."""
        self.animation_controller.pause()
        print("Animation paused")

    def on_reset(self):
        """Handle reset button click."""
        # Reset animation
        self.animation_controller.reset()

        # Reset visualization to original array
        self.visualization_canvas.set_array(self.current_array)

        # Clear messages
        self.legend_panel.clear_messages()

        print("Animation reset")

    def on_speed_change(self, speed: float):
        """Handle speed slider change."""
        self.animation_controller.set_speed(speed)
        print(f"Speed changed to {speed}x")

    def on_animation_update(
        self,
        action: str,
        indices: list,
        description: str,
        animation_data: Optional[dict] = None,
    ):
        """Handle animation frame updates."""
        # Update visualization
        self.visualization_canvas.update_animation(
            action, indices, description, animation_data
        )

    def on_step_change(self, step_number: int, description: str):
        """Handle animation step changes."""
        # Update progress display
        current, total = self.animation_controller.get_progress()
        self.control_panel.update_progress(current, total)
        self.control_panel.update_operation(description)

    def on_animation_complete(self):
        """Handle animation completion."""
        # Calculate statistics
        animation_time = time.time() - self.animation_start_time
        current, total = self.animation_controller.get_progress()

        # Show completion message
        self.legend_panel.show_completion_message("Sort Complete!")
        self.legend_panel.flash_completion()

        # Show statistics
        stats = {"total_steps": total, "time_taken": animation_time}
        self.legend_panel.show_statistics(stats)

        # Highlight completion in visualization
        self.visualization_canvas.highlight_completion()

        # Update control panel
        self.control_panel.on_animation_complete()

        print(f"Animation completed in {animation_time:.2f}s with {total} steps")

    def on_closing(self):
        """Handle application closing."""
        # Clean up animation controller
        self.animation_controller.cleanup()

        # Destroy window
        self.root.destroy()

    def run(self):
        """Start the application main loop."""
        try:
            print("Starting Sorting Algorithm Visualizer...")
            self.root.mainloop()
        except KeyboardInterrupt:
            print("Application interrupted by user")
        except Exception as e:
            print(f"Application error: {e}")
            messagebox.showerror("Application Error", f"An error occurred: {str(e)}")
        finally:
            self.on_closing()


def main():
    """Main entry point for the application."""
    try:
        app = SortingVisualizerApp()
        app.run()
    except Exception as e:
        print(f"Failed to start application: {e}")
        if "--debug" in sys.argv:
            raise
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
