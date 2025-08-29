# Constants for the Sorting Visualizer Application

# Window dimensions
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# Panel dimensions
CONTROL_PANEL_WIDTH = 250
VISUALIZATION_CANVAS_WIDTH = 700
LEGEND_PANEL_WIDTH = 130
CANVAS_HEIGHT = 400

# Colors
COLORS = {
    "DEFAULT": "#3498DB",  # Blue - unsorted bars
    "COMPARING": "#F39C12",  # Orange - bars being compared
    "SWAPPING": "#E74C3C",  # Red - bars being swapped
    "SORTED": "#27AE60",  # Green - sorted bars
    "BACKGROUND": "#2C3E50",  # Dark blue-gray background
    "PANEL_BG": "#34495E",  # Slightly lighter panel background
    "TEXT": "#FFFFFF",  # White text
    "ERROR": "#E74C3C",  # Red error text
    "SUCCESS": "#27AE60",  # Green success text
}

# Animation settings
ANIMATION_SPEED_DEFAULT = 1.0
ANIMATION_SPEED_MIN = 0.5
ANIMATION_SPEED_MAX = 3.0
FPS_TARGET = 60
FRAME_INTERVAL_MS = 16  # 1000ms / 60fps ≈ 16ms
INTERPOLATION_FRAMES = 8

# Array settings
ARRAY_SIZE_DEFAULT = 25
ARRAY_SIZE_MIN = 10
ARRAY_SIZE_MAX = 50
VALUE_MIN = 1
VALUE_MAX = 100

# UI spacing and sizing
PADDING = 10
BAR_SPACING = 10
BUTTON_HEIGHT = 30
SLIDER_WIDTH = 200

# Control panel layout
CONTROL_Y_START = 20
CONTROL_SPACING = 15

# Canvas settings
CANVAS_PADDING = 20
BAR_TEXT_OFFSET = 5

# Algorithm complexities and descriptions
ALGORITHM_INFO = {
    "Bubble Sort": {
        "time_complexity": "O(n²)",
        "space_complexity": "O(1)",
        "description": "Compares adjacent elements and swaps them if they are in wrong order.",
    },
    "Selection Sort": {
        "time_complexity": "O(n²)",
        "space_complexity": "O(1)",
        "description": "Finds the minimum element and places it at the beginning.",
    },
    "Insertion Sort": {
        "time_complexity": "O(n²)",
        "space_complexity": "O(1)",
        "description": "Inserts each element into its correct position in the sorted portion.",
    },
    "Merge Sort": {
        "time_complexity": "O(n log n)",
        "space_complexity": "O(n)",
        "description": "Divides array into halves, sorts them, then merges back together.",
    },
    "Quick Sort": {
        "time_complexity": "O(n log n)",
        "space_complexity": "O(log n)",
        "description": "Partitions array around a pivot, then sorts partitions recursively.",
    },
}

# Error messages
ERROR_MESSAGES = {
    "EMPTY_INPUT": "Please enter at least one number.",
    "INVALID_FORMAT": "Please enter comma-separated integers only.",
    "OUT_OF_RANGE": f"Numbers must be between {VALUE_MIN} and {VALUE_MAX}.",
    "TOO_MANY_ELEMENTS": f"Maximum {ARRAY_SIZE_MAX} elements allowed.",
    "INVALID_NUMBER": "Invalid number format detected.",
    "NO_ALGORITHM": "Please select an algorithm first.",
}

# Button symbols and text
BUTTON_SYMBOLS = {"PLAY": "▶", "PAUSE": "⏸", "RESET": "⟲"}

# Legend items
LEGEND_ITEMS = [
    ("Unsorted", COLORS["DEFAULT"]),
    ("Comparing", COLORS["COMPARING"]),
    ("Swapping", COLORS["SWAPPING"]),
    ("Sorted", COLORS["SORTED"]),
]
