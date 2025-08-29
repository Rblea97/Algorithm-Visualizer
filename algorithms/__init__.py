from .bubble_sort import BubbleSort
from .selection_sort import SelectionSort
from .insertion_sort import InsertionSort
from .merge_sort import MergeSort
from .quick_sort import QuickSort

# Dictionary mapping algorithm names to their classes
ALGORITHMS = {
    "Bubble Sort": BubbleSort,
    "Selection Sort": SelectionSort,
    "Insertion Sort": InsertionSort,
    "Merge Sort": MergeSort,
    "Quick Sort": QuickSort,
}
