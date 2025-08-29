"""
Pytest configuration and fixtures for Algorithm Visualizer tests.

Handles GUI testing compatibility, headless environments, and test setup.
"""

import os
import sys
import pytest
import tkinter as tk
from unittest.mock import patch


def is_headless_environment():
    """
    Detect if we're running in a headless environment.
    
    Returns:
        bool: True if headless (no display available)
    """
    # Check common CI environment variables
    ci_indicators = ['CI', 'CONTINUOUS_INTEGRATION', 'GITHUB_ACTIONS', 'TRAVIS', 'JENKINS_URL']
    if any(os.environ.get(var) for var in ci_indicators):
        return True
    
    # Check for display availability on Unix systems
    if sys.platform.startswith('linux') and not os.environ.get('DISPLAY'):
        return True
    
    # Try to create a test Tk instance
    try:
        test_root = tk.Tk()
        test_root.withdraw()
        test_root.destroy()
        return False
    except tk.TclError:
        return True


@pytest.fixture(scope="session")
def headless_environment():
    """Session-scoped fixture to detect headless environment once."""
    return is_headless_environment()


@pytest.fixture(autouse=True)
def gui_environment_check(request, headless_environment):
    """
    Automatically check if GUI tests can run in current environment.
    
    Skips tests marked with @pytest.mark.gui if running in headless environment
    without proper display setup.
    """
    if request.node.get_closest_marker('gui') and headless_environment:
        pytest.skip("GUI test skipped in headless environment")


@pytest.fixture
def mock_tkinter_root():
    """
    Fixture that provides a mocked Tkinter root for headless testing.
    
    Returns a mock object that can be used instead of tk.Tk() in tests.
    """
    from unittest.mock import MagicMock
    
    mock_root = MagicMock()
    mock_root.withdraw.return_value = None
    mock_root.destroy.return_value = None
    mock_root.after.return_value = "mock_after_id"
    mock_root.after_cancel.return_value = None
    mock_root.update.return_value = None
    mock_root.mainloop.return_value = None
    
    return mock_root


@pytest.fixture
def safe_tkinter_root(headless_environment):
    """
    Fixture that provides a safe Tkinter root, mocked in headless environments.
    
    Returns:
        Either a real tk.Tk() instance or a mock, depending on environment
    """
    if headless_environment:
        from unittest.mock import MagicMock
        mock_root = MagicMock()
        mock_root.withdraw.return_value = None
        mock_root.destroy.return_value = None
        yield mock_root
    else:
        root = tk.Tk()
        root.withdraw()  # Hide window
        try:
            yield root
        finally:
            try:
                root.destroy()
            except tk.TclError:
                pass  # Already destroyed


class HeadlessTestMixin:
    """
    Mixin class for test classes that need GUI compatibility.
    
    Provides helper methods for handling GUI tests in headless environments.
    """
    
    def create_safe_root(self, headless_environment=None):
        """Create a root that works in both GUI and headless environments."""
        if headless_environment is None:
            headless_environment = is_headless_environment()
            
        if headless_environment:
            from unittest.mock import MagicMock
            mock_root = MagicMock()
            mock_root.withdraw.return_value = None
            mock_root.destroy.return_value = None
            mock_root.after.return_value = "mock_after_id"
            mock_root.after_cancel.return_value = None
            return mock_root
        else:
            root = tk.Tk()
            root.withdraw()
            return root
    
    def cleanup_root(self, root):
        """Safely clean up a root window."""
        if hasattr(root, 'destroy') and callable(root.destroy):
            try:
                if not isinstance(root.destroy, MagicMock):
                    root.destroy()
            except (tk.TclError, AttributeError):
                pass


# Pytest markers for different test categories
pytestmark = [
    pytest.mark.filterwarnings("ignore::DeprecationWarning"),
    pytest.mark.filterwarnings("ignore::PendingDeprecationWarning"),
]