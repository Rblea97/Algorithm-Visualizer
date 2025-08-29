from typing import List, Tuple
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.base_algorithm import SortingAlgorithm


class QuickSort(SortingAlgorithm):
    """
    Quick Sort implementation with step-by-step animation support.

    Partitions array around a pivot element, then sorts the partitions
    recursively. Uses last element as pivot.
    """

    def get_name(self) -> str:
        return "Quick Sort"

    def get_steps(self, arr: List[int]) -> List[Tuple[str, List[int], str]]:
        """Generate animation steps for quick sort."""
        steps = []
        arr_copy = arr.copy()

        def quick_sort_helper(low: int, high: int):
            if low < high:
                # Partition the array and get pivot index
                pivot_idx = partition(low, high)

                # Mark pivot as in correct position
                steps.append(
                    (
                        "mark_sorted",
                        [pivot_idx],
                        f"Pivot {arr_copy[pivot_idx]} is now in correct position",
                    )
                )

                # Recursively sort elements before and after partition
                quick_sort_helper(low, pivot_idx - 1)
                quick_sort_helper(pivot_idx + 1, high)

        def partition(low: int, high: int) -> int:
            # Choose rightmost element as pivot
            pivot = arr_copy[high]
            steps.append(("highlight_pivot", [high], f"Choosing {pivot} as pivot"))

            # Index of smaller element (indicates right position of pivot)
            i = low - 1

            for j in range(low, high):
                # Compare current element with pivot
                steps.append(
                    (
                        "compare",
                        [j, high],
                        f"Comparing {arr_copy[j]} with pivot {pivot}",
                    )
                )

                # If current element is smaller than or equal to pivot
                if arr_copy[j] <= pivot:
                    i += 1
                    if i != j:
                        steps.append(
                            (
                                "swap",
                                [i, j],
                                f"Swapping {arr_copy[i]} and {arr_copy[j]}",
                            )
                        )
                        arr_copy[i], arr_copy[j] = arr_copy[j], arr_copy[i]

            # Place pivot in correct position
            if i + 1 != high:
                steps.append(
                    (
                        "swap",
                        [i + 1, high],
                        f"Placing pivot {pivot} in correct position",
                    )
                )
                arr_copy[i + 1], arr_copy[high] = arr_copy[high], arr_copy[i + 1]

            return i + 1

        quick_sort_helper(0, len(arr_copy) - 1)

        # Mark all elements as sorted at the end
        steps.append(
            ("mark_sorted", list(range(len(arr_copy))), "All elements are now sorted")
        )

        return steps

    def get_complexity(self) -> Tuple[str, str]:
        """Return time and space complexity."""
        return ("O(n log n)", "O(log n)")

    def get_description(self) -> str:
        """Return algorithm description."""
        return "Partitions array around a pivot element, then sorts the partitions recursively."
