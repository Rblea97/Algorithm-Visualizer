"""
Unit tests for AnimationController class.

Tests cover animation state management, timing control, callback functionality,
and proper cleanup of resources.
"""

import pytest
import tkinter as tk
import time
from unittest.mock import Mock, MagicMock
from utils.animation_controller import AnimationController
from utils.constants import (
    ANIMATION_SPEED_DEFAULT,
    ANIMATION_SPEED_MIN, 
    ANIMATION_SPEED_MAX,
    INTERPOLATION_FRAMES
)
from .conftest import HeadlessTestMixin


@pytest.mark.gui
class TestAnimationController(HeadlessTestMixin):
    """Test cases for AnimationController functionality."""
    
    def setup_method(self):
        """Setup test environment before each test."""
        # Create a safe tkinter root for testing
        self.root = self.create_safe_root()
        
        # Create mock callback
        self.mock_callback = Mock()
        
        # Create animation controller
        self.controller = AnimationController(self.root, self.mock_callback)
        
        # Sample animation steps for testing
        self.test_steps = [
            ("compare", [0, 1], "Comparing elements 0 and 1"),
            ("swap", [0, 1], "Swapping elements 0 and 1"),
            ("mark_sorted", [0], "Element 0 is sorted")
        ]
    
    def teardown_method(self):
        """Cleanup after each test."""
        if hasattr(self, 'controller'):
            self.controller.cleanup()
        if hasattr(self, 'root'):
            self.cleanup_root(self.root)
    
    def test_initialization(self):
        """Test controller initialization."""
        assert self.controller.root is self.root
        assert self.controller.update_callback is self.mock_callback
        assert not self.controller.is_playing
        assert not self.controller.is_paused
        assert self.controller.current_step == 0
        assert self.controller.animation_steps == []
        assert self.controller.speed == ANIMATION_SPEED_DEFAULT
    
    def test_set_steps(self):
        """Test setting animation steps."""
        self.controller.set_steps(self.test_steps)
        
        assert self.controller.animation_steps == self.test_steps
        assert self.controller.current_step == 0
        assert self.controller.interpolation_frame == 0
    
    def test_speed_control(self):
        """Test speed setting and bounds."""
        # Test valid speed
        self.controller.set_speed(2.0)
        assert self.controller.speed == 2.0
        
        # Test minimum bound
        self.controller.set_speed(0.1)
        assert self.controller.speed == ANIMATION_SPEED_MIN
        
        # Test maximum bound
        self.controller.set_speed(10.0)
        assert self.controller.speed == ANIMATION_SPEED_MAX
        
        # Test negative speed
        self.controller.set_speed(-1.0)
        assert self.controller.speed == ANIMATION_SPEED_MIN
    
    def test_frame_interval_calculation(self):
        """Test frame interval calculation based on speed."""
        self.controller.set_speed(1.0)
        interval_1x = self.controller.get_frame_interval()
        
        self.controller.set_speed(2.0)
        interval_2x = self.controller.get_frame_interval()
        
        # Higher speed should result in shorter interval
        assert interval_2x < interval_1x
        assert isinstance(interval_1x, int)
        assert isinstance(interval_2x, int)
        assert interval_1x > 0
        assert interval_2x > 0
    
    def test_progress_tracking(self):
        """Test progress tracking functionality."""
        self.controller.set_steps(self.test_steps)
        
        current, total = self.controller.get_progress()
        assert current == 0
        assert total == len(self.test_steps)
        
        # Simulate advancing steps
        self.controller.current_step = 2
        current, total = self.controller.get_progress()
        assert current == 2
        assert total == len(self.test_steps)
    
    def test_state_management(self):
        """Test play/pause/stop state management."""
        # Initial state
        assert not self.controller.is_running()
        
        # Test empty steps
        self.controller.play()
        assert not self.controller.is_playing
        
        # Set steps and test play
        self.controller.set_steps(self.test_steps)
        self.controller.play()
        assert self.controller.is_playing
        assert not self.controller.is_paused
        assert self.controller.is_running()
        
        # Test pause
        self.controller.pause()
        assert not self.controller.is_playing
        assert self.controller.is_paused
        assert not self.controller.is_running()
        
        # Test stop
        self.controller.stop()
        assert not self.controller.is_playing
        assert not self.controller.is_paused
        assert not self.controller.is_running()
        assert self.controller.current_step == 0
    
    def test_reset_functionality(self):
        """Test reset functionality."""
        self.controller.set_steps(self.test_steps)
        self.controller.current_step = 2
        self.controller.interpolation_frame = 5
        
        self.controller.reset()
        
        assert self.controller.current_step == 0
        assert self.controller.interpolation_frame == 0
        assert not self.controller.is_playing
        assert not self.controller.is_paused
        
        # Should call update callback with reset
        self.mock_callback.assert_called_with("reset", [], "Reset to initial state")
    
    def test_callback_registration(self):
        """Test callback registration and calling."""
        step_callback = Mock()
        completion_callback = Mock()
        
        self.controller.set_step_callback(step_callback)
        self.controller.set_completion_callback(completion_callback)
        
        assert self.controller.on_step_change is step_callback
        assert self.controller.on_completion is completion_callback
    
    def test_cleanup(self):
        """Test proper cleanup of resources."""
        self.controller.set_steps(self.test_steps)
        self.controller.play()
        
        # Should have scheduled frames
        assert self.controller.is_playing
        
        self.controller.cleanup()
        
        assert not self.controller.is_playing
        assert not self.controller.is_paused
        assert self.controller.after_id is None
    
    def test_empty_steps_handling(self):
        """Test handling of empty step list."""
        self.controller.set_steps([])
        
        current, total = self.controller.get_progress()
        assert current == 0
        assert total == 0
        
        # Should not start playing with empty steps
        self.controller.play()
        assert not self.controller.is_playing
    
    def test_single_step_animation(self):
        """Test animation with single step."""
        single_step = [("compare", [0, 1], "Single comparison")]
        self.controller.set_steps(single_step)
        
        current, total = self.controller.get_progress()
        assert current == 0
        assert total == 1
        
        # Should be able to start animation
        self.controller.play()
        assert self.controller.is_playing


@pytest.mark.gui
class TestAnimationControllerIntegration(HeadlessTestMixin):
    """Integration tests for AnimationController with mock UI updates."""
    
    def setup_method(self):
        """Setup test environment."""
        self.root = self.create_safe_root()
        
        self.update_calls = []
        
        def mock_update(action, indices, description, animation_data=None):
            self.update_calls.append({
                'action': action,
                'indices': indices,
                'description': description,
                'animation_data': animation_data
            })
        
        self.controller = AnimationController(self.root, mock_update)
        
        # Simple test steps
        self.test_steps = [
            ("compare", [0, 1], "Compare 0 and 1"),
            ("swap", [0, 1], "Swap 0 and 1")
        ]
    
    def teardown_method(self):
        """Cleanup."""
        if hasattr(self, 'controller'):
            self.controller.cleanup()
        if hasattr(self, 'root'):
            self.cleanup_root(self.root)
    
    def test_animation_data_structure(self):
        """Test that animation data is properly structured."""
        self.controller.set_steps(self.test_steps)
        
        step_calls = []
        completion_calls = []
        
        def step_callback(step_num, description):
            step_calls.append((step_num, description))
        
        def completion_callback():
            completion_calls.append("completed")
        
        self.controller.set_step_callback(step_callback)
        self.controller.set_completion_callback(completion_callback)
        
        # Set very fast speed to minimize test time
        self.controller.set_speed(ANIMATION_SPEED_MAX)
        
        # Start animation
        self.controller.play()
        
        # Let a few frames execute
        for _ in range(5):
            self.root.update()
            time.sleep(0.001)  # Very short sleep
        
        # Check that update calls were made
        if self.update_calls:
            call = self.update_calls[0]
            assert 'action' in call
            assert 'indices' in call
            assert 'description' in call
            assert 'animation_data' in call
            
            if call['animation_data']:
                data = call['animation_data']
                assert 'progress' in data
                assert 'interpolation_frame' in data
                assert 'is_final_frame' in data
                assert 0.0 <= data['progress'] <= 1.0
                assert isinstance(data['interpolation_frame'], int)
                assert isinstance(data['is_final_frame'], bool)
    
    def test_step_progression(self):
        """Test that steps progress correctly."""
        self.controller.set_steps(self.test_steps)
        
        initial_current, total = self.controller.get_progress()
        assert initial_current == 0
        assert total == len(self.test_steps)
        
        # Manually advance a step for testing
        self.controller.current_step = 1
        
        current, total = self.controller.get_progress()
        assert current == 1
        assert total == len(self.test_steps)


@pytest.mark.gui
class TestAnimationControllerErrorHandling(HeadlessTestMixin):
    """Test error handling and edge cases."""
    
    def setup_method(self):
        """Setup test environment."""
        self.root = self.create_safe_root()
        self.controller = AnimationController(self.root, Mock())
    
    def teardown_method(self):
        """Cleanup."""
        if hasattr(self, 'controller'):
            self.controller.cleanup()
        if hasattr(self, 'root'):
            self.cleanup_root(self.root)
    
    def test_malformed_steps(self):
        """Test handling of malformed animation steps."""
        # Test with steps that don't have expected structure
        malformed_steps = [
            ("compare",),  # Missing indices and description
            ("swap", [0, 1]),  # Missing description
            ("invalid", [0, 1], "description", "extra")  # Extra element
        ]
        
        # Controller should accept these without crashing
        self.controller.set_steps(malformed_steps)
        current, total = self.controller.get_progress()
        assert total == len(malformed_steps)
    
    def test_invalid_indices(self):
        """Test handling of invalid indices in steps."""
        invalid_steps = [
            ("compare", [-1, 0], "Invalid negative index"),
            ("swap", [0, 1000], "Very large index"),
            ("mark_sorted", [], "Empty indices list")
        ]
        
        # Should not crash when setting steps
        self.controller.set_steps(invalid_steps)
        assert len(self.controller.animation_steps) == len(invalid_steps)
    
    def test_none_callback(self):
        """Test behavior with None callbacks."""
        # Should not crash with None callbacks
        self.controller.set_step_callback(None)
        self.controller.set_completion_callback(None)
        
        self.controller.set_steps([("test", [0], "Test step")])
        self.controller.play()
        
        # Should still work without callbacks
        assert self.controller.is_playing
    
    def test_destroyed_root(self):
        """Test behavior when root is destroyed during animation."""
        self.controller.set_steps([("test", [0], "Test")])
        self.controller.play()
        
        # Destroy root
        self.root.destroy()
        
        # Cleanup should not crash
        self.controller.cleanup()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])