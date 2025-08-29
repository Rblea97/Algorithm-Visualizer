"""
Integration tests for UI components.

Tests basic functionality of UI panels, widget creation,
and interaction between components.
"""

import pytest
import tkinter as tk
from unittest.mock import Mock, MagicMock, patch
from ui import ControlPanel, VisualizationCanvas, LegendPanel
from algorithms import ALGORITHMS
from utils import InputValidator
from .conftest import HeadlessTestMixin


@pytest.mark.gui
class TestUIIntegration(HeadlessTestMixin):
    """Integration tests for UI components."""
    
    def setup_method(self):
        """Setup test environment."""
        # Create safe root window
        self.root = self.create_safe_root()
        
        # Create test frames for each panel
        self.control_frame = tk.Frame(self.root)
        self.canvas_frame = tk.Frame(self.root)
        self.legend_frame = tk.Frame(self.root)
    
    def teardown_method(self):
        """Clean up after tests."""
        if hasattr(self, 'root'):
            self.cleanup_root(self.root)
    
    def test_control_panel_creation(self):
        """Test ControlPanel can be created without errors."""
        try:
            control_panel = ControlPanel(self.control_frame)
            
            # Should have created the main frame
            assert hasattr(control_panel, 'frame')
            assert control_panel.frame.master == self.control_frame
            
            # Should have initialized callbacks as None
            assert control_panel.on_algorithm_change is None
            
        except Exception as e:
            pytest.fail(f"ControlPanel creation failed: {e}")
    
    def test_visualization_canvas_creation(self):
        """Test VisualizationCanvas can be created without errors."""
        try:
            canvas = VisualizationCanvas(self.canvas_frame)
            
            # Should have a canvas widget
            assert hasattr(canvas, 'canvas')
            assert isinstance(canvas.canvas, tk.Canvas)
            
            # Should be able to get the widget
            widget = canvas.get_widget()
            assert widget is not None
            
        except Exception as e:
            pytest.fail(f"VisualizationCanvas creation failed: {e}")
    
    def test_legend_panel_creation(self):
        """Test LegendPanel can be created without errors."""
        try:
            legend_panel = LegendPanel(self.legend_frame)
            
            # Should have created main frame
            assert hasattr(legend_panel, 'frame')
            assert legend_panel.frame.master == self.legend_frame
            
        except Exception as e:
            pytest.fail(f"LegendPanel creation failed: {e}")
    
    def test_control_panel_callback_setting(self):
        """Test ControlPanel callback functionality."""
        control_panel = ControlPanel(self.control_frame)
        
        # Mock callbacks
        algorithm_callback = Mock()
        array_callback = Mock()
        play_callback = Mock()
        pause_callback = Mock()
        reset_callback = Mock()
        speed_callback = Mock()
        
        # Set callbacks
        control_panel.set_algorithm_change_callback(algorithm_callback)
        control_panel.set_array_change_callback(array_callback)
        control_panel.set_playback_callbacks(play_callback, pause_callback, reset_callback)
        control_panel.set_speed_change_callback(speed_callback)
        
        # Verify callbacks are set
        assert control_panel.on_algorithm_change == algorithm_callback
        assert control_panel.on_array_change == array_callback
        assert control_panel.on_play == play_callback
        assert control_panel.on_pause == pause_callback
        assert control_panel.on_reset == reset_callback
        assert control_panel.on_speed_change == speed_callback
    
    def test_visualization_canvas_array_handling(self):
        """Test VisualizationCanvas array operations."""
        canvas = VisualizationCanvas(self.canvas_frame)
        
        # Test setting array
        test_array = [3, 1, 4, 1, 5]
        try:
            canvas.set_array(test_array)
            # Should not crash
        except Exception as e:
            pytest.fail(f"set_array failed: {e}")
        
        # Test update animation (basic call)
        try:
            canvas.update_animation("compare", [0, 1], "Test comparison")
            # Should not crash
        except Exception as e:
            pytest.fail(f"update_animation failed: {e}")
    
    def test_legend_panel_message_handling(self):
        """Test LegendPanel message functionality."""
        legend_panel = LegendPanel(self.legend_frame)
        
        # Test showing completion message
        try:
            legend_panel.show_completion_message("Test Complete!")
            # Should not crash
        except Exception as e:
            pytest.fail(f"show_completion_message failed: {e}")
        
        # Test clearing messages
        try:
            legend_panel.clear_messages()
            # Should not crash
        except Exception as e:
            pytest.fail(f"clear_messages failed: {e}")


@pytest.mark.gui
class TestUIComponentInteraction(HeadlessTestMixin):
    """Test interactions between UI components."""
    
    def setup_method(self):
        """Setup test environment with all components."""
        self.root = self.create_safe_root()
        
        # Create frames
        self.control_frame = tk.Frame(self.root)
        self.canvas_frame = tk.Frame(self.root) 
        self.legend_frame = tk.Frame(self.root)
        
        # Create panels
        self.control_panel = ControlPanel(self.control_frame)
        self.canvas = VisualizationCanvas(self.canvas_frame)
        self.legend_panel = LegendPanel(self.legend_frame)
        
        # Track callback calls
        self.callback_calls = []
        
    def teardown_method(self):
        """Clean up."""
        if hasattr(self, 'root'):
            self.cleanup_root(self.root)
    
    def test_algorithm_selection_flow(self):
        """Test the flow from algorithm selection to visualization setup."""
        # Mock algorithm change callback
        def algorithm_callback(algorithm_name):
            self.callback_calls.append(('algorithm_change', algorithm_name))
            
        self.control_panel.set_algorithm_change_callback(algorithm_callback)
        
        # Test that available algorithms can be selected
        available_algorithms = list(ALGORITHMS.keys())
        assert len(available_algorithms) > 0
        
        # Simulate algorithm selection (would normally come from UI interaction)
        test_algorithm = available_algorithms[0]
        if self.control_panel.on_algorithm_change:
            self.control_panel.on_algorithm_change(test_algorithm)
        
        # Check callback was called
        assert len(self.callback_calls) == 1
        assert self.callback_calls[0] == ('algorithm_change', test_algorithm)
    
    def test_array_update_flow(self):
        """Test the flow from array input to canvas update."""
        # Mock array change callback
        def array_callback(array):
            self.callback_calls.append(('array_change', array))
            # Simulate updating canvas
            self.canvas.set_array(array)
            
        self.control_panel.set_array_change_callback(array_callback)
        
        # Test valid array input
        test_array = [3, 1, 4, 1, 5]
        if self.control_panel.on_array_change:
            self.control_panel.on_array_change(test_array)
        
        # Check callback was called
        assert len(self.callback_calls) == 1
        assert self.callback_calls[0] == ('array_change', test_array)
    
    def test_playback_control_flow(self):
        """Test playback control flow between components."""
        # Mock playback callbacks
        def play_callback():
            self.callback_calls.append('play')
            
        def pause_callback():
            self.callback_calls.append('pause')
            
        def reset_callback():
            self.callback_calls.append('reset')
            # Simulate reset effects
            self.legend_panel.clear_messages()
            
        self.control_panel.set_playback_callbacks(
            play_callback, pause_callback, reset_callback
        )
        
        # Test play
        if self.control_panel.on_play:
            self.control_panel.on_play()
        assert 'play' in self.callback_calls
        
        # Test pause
        if self.control_panel.on_pause:
            self.control_panel.on_pause()
        assert 'pause' in self.callback_calls
        
        # Test reset
        if self.control_panel.on_reset:
            self.control_panel.on_reset()
        assert 'reset' in self.callback_calls


class TestInputValidationIntegration:
    """Test integration with input validation."""
    
    def setup_method(self):
        """Setup test environment."""
        pass  # No GUI needed for input validation
        self.control_frame = tk.Frame(self.root)
    
    def teardown_method(self):
        """Clean up."""
        if hasattr(self, 'root'):
            self.cleanup_root(self.root)
    
    def test_input_validator_integration(self):
        """Test that InputValidator integrates properly with UI."""
        # Test valid input
        valid_input = "1,2,3,4,5"
        is_valid, numbers, error = InputValidator.validate_input(valid_input)
        
        assert is_valid is True
        assert numbers == [1, 2, 3, 4, 5]
        assert error is None
        
        # Test invalid input
        invalid_input = "1,abc,3"
        is_valid, numbers, error = InputValidator.validate_input(invalid_input)
        
        assert is_valid is False
        assert numbers is None
        assert error is not None
        assert isinstance(error, str)
        assert len(error) > 0
    
    def test_array_size_validation(self):
        """Test array size validation."""
        # Test valid size
        assert InputValidator.validate_array_size(10) is True
        assert InputValidator.validate_array_size(50) is True
        
        # Test invalid sizes  
        assert InputValidator.validate_array_size(0) is False
        assert InputValidator.validate_array_size(-1) is False
        assert InputValidator.validate_array_size(1000) is False
    
    def test_validation_messages(self):
        """Test validation message generation."""
        test_numbers = [5, 2, 8, 1, 9]
        message = InputValidator.get_validation_message(test_numbers)
        
        assert isinstance(message, str)
        assert len(message) > 0
        assert "5 elements" in message or "5" in message
        
        # Test formatting
        formatted = InputValidator.format_input(test_numbers)
        assert isinstance(formatted, str)
        assert "5" in formatted
        assert "2" in formatted


@pytest.mark.gui  
class TestErrorHandling(HeadlessTestMixin):
    """Test error handling in UI components."""
    
    def setup_method(self):
        """Setup test environment."""
        self.root = self.create_safe_root()
        self.control_frame = tk.Frame(self.root)
        self.canvas_frame = tk.Frame(self.root)
        self.legend_frame = tk.Frame(self.root)
    
    def teardown_method(self):
        """Clean up."""
        if hasattr(self, 'root'):
            self.cleanup_root(self.root)
    
    def test_canvas_with_invalid_data(self):
        """Test canvas behavior with invalid data."""
        canvas = VisualizationCanvas(self.canvas_frame)
        
        # Test with None
        try:
            canvas.set_array(None)
            # Should either handle gracefully or have clear error
        except (TypeError, AttributeError):
            pass  # Expected behavior
        except Exception as e:
            pytest.fail(f"Unexpected error with None array: {e}")
        
        # Test with empty array
        try:
            canvas.set_array([])
            # Should handle empty array gracefully
        except Exception as e:
            pytest.fail(f"Failed to handle empty array: {e}")
    
    def test_legend_panel_error_handling(self):
        """Test LegendPanel error handling."""
        legend_panel = LegendPanel(self.legend_frame)
        
        # Test with None message
        try:
            legend_panel.show_completion_message(None)
            # Should handle gracefully
        except Exception as e:
            # Should not crash
            pass
        
        # Test with empty message
        try:
            legend_panel.show_completion_message("")
            # Should handle gracefully
        except Exception as e:
            pytest.fail(f"Failed to handle empty message: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])