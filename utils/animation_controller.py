import tkinter as tk
from typing import List, Tuple, Callable, Dict, Any, Optional
from .constants import (
    FRAME_INTERVAL_MS,
    INTERPOLATION_FRAMES,
    ANIMATION_SPEED_DEFAULT,
    ANIMATION_SPEED_MIN,
    ANIMATION_SPEED_MAX,
)


class AnimationController:
    """
    Controls smooth animations for the sorting visualizer.

    Manages animation timing, interpolation, and state transitions
    using tkinter's after() method for non-blocking execution.
    """

    def __init__(self, root: tk.Tk, update_callback: Callable):
        """
        Initialize animation controller.

        Args:
            root: Main tkinter window
            update_callback: Function to call for each animation frame
        """
        self.root = root
        self.update_callback = update_callback

        # Animation state
        self.is_playing = False
        self.is_paused = False
        self.current_step = 0
        self.animation_steps: List[Tuple[str, List[int], str]] = []
        self.speed = ANIMATION_SPEED_DEFAULT

        # Animation timing
        self.after_id: Optional[str] = None
        self.interpolation_frame = 0
        self.current_animation_data: Optional[Dict[str, Any]] = None

        # Callbacks
        self.on_step_change: Optional[Callable[[int, str]]] = None
        self.on_completion: Optional[Callable] = None

    def set_steps(self, steps: List[Tuple[str, List[int], str]]):
        """
        Set the animation steps to be executed.

        Args:
            steps: List of animation steps from sorting algorithm
        """
        self.animation_steps = steps
        self.current_step = 0
        self.interpolation_frame = 0
        self.current_animation_data = None

    def set_speed(self, speed: float):
        """
        Set animation speed multiplier.

        Args:
            speed: Speed multiplier (0.5 to 3.0)
        """
        self.speed = max(ANIMATION_SPEED_MIN, min(ANIMATION_SPEED_MAX, speed))

    def get_frame_interval(self) -> int:
        """
        Calculate frame interval based on current speed.

        Returns:
            Frame interval in milliseconds
        """
        return int(FRAME_INTERVAL_MS / self.speed)

    def play(self):
        """Start or resume animation."""
        if not self.animation_steps:
            return

        self.is_playing = True
        self.is_paused = False
        self._schedule_next_frame()

    def pause(self):
        """Pause animation."""
        self.is_paused = True
        self.is_playing = False
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None

    def stop(self):
        """Stop animation and reset to beginning."""
        self.is_playing = False
        self.is_paused = False
        self.current_step = 0
        self.interpolation_frame = 0
        self.current_animation_data = None

        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None

    def reset(self):
        """Reset animation to initial state."""
        self.stop()
        if self.update_callback:
            # Clear any highlighting/coloring
            self.update_callback("reset", [], "Reset to initial state")

    def is_running(self) -> bool:
        """Check if animation is currently running."""
        return self.is_playing and not self.is_paused

    def get_progress(self) -> Tuple[int, int]:
        """
        Get current progress.

        Returns:
            Tuple of (current_step, total_steps)
        """
        return (self.current_step, len(self.animation_steps))

    def set_step_callback(self, callback: Callable[[int, str], None]):
        """
        Set callback for step changes.

        Args:
            callback: Function called with (step_number, description)
        """
        self.on_step_change = callback

    def set_completion_callback(self, callback: Callable[[], None]):
        """
        Set callback for animation completion.

        Args:
            callback: Function called when animation completes
        """
        self.on_completion = callback

    def _schedule_next_frame(self):
        """Schedule the next animation frame."""
        if not self.is_playing or self.is_paused:
            return

        interval = self.get_frame_interval()
        self.after_id = self.root.after(interval, self._execute_frame)

    def _execute_frame(self):
        """Execute a single animation frame."""
        if not self.is_playing or self.is_paused:
            return

        # Check if we've completed all steps
        if self.current_step >= len(self.animation_steps):
            self._complete_animation()
            return

        # Get current step
        action, indices, description = self.animation_steps[self.current_step]

        # Handle interpolation for smooth animations
        if self.interpolation_frame == 0:
            # Start of new step - report correct step number
            if self.on_step_change:
                step_number = self.current_step + 1
                self.on_step_change(step_number, description)

        # Calculate interpolation progress (0.0 to 1.0)
        progress = self.interpolation_frame / INTERPOLATION_FRAMES

        # Create animation data with interpolation info
        animation_data = {
            "action": action,
            "indices": indices,
            "description": description,
            "progress": progress,
            "interpolation_frame": self.interpolation_frame,
            "is_final_frame": self.interpolation_frame == INTERPOLATION_FRAMES - 1,
        }

        # Call update callback
        if self.update_callback:
            self.update_callback(action, indices, description, animation_data)

        # Advance interpolation frame
        self.interpolation_frame += 1

        # Check if we've completed this step's interpolation
        if self.interpolation_frame >= INTERPOLATION_FRAMES:
            self.current_step += 1
            self.interpolation_frame = 0

        # Schedule next frame
        self._schedule_next_frame()

    def _complete_animation(self):
        """Handle animation completion."""
        self.is_playing = False
        self.is_paused = False
        self.after_id = None

        # Ensure final step progress is reported correctly
        if self.on_step_change and self.animation_steps:
            total_steps = len(self.animation_steps)
            self.on_step_change(total_steps, "Animation completed")

        # Call completion callback
        if self.on_completion:
            self.on_completion()

    def cleanup(self):
        """Clean up animation controller resources."""
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None

        self.is_playing = False
        self.is_paused = False
