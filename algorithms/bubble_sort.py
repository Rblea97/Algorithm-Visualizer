from typing import List, Tuple
from .base_algorithm import SortingAlgorithm


class BubbleSort(SortingAlgorithm):
    """
    Bubble Sort implementation with step-by-step animation support.

    Compares adjacent elements and swaps them if they are in wrong order.
    Process repeats until no more swaps are needed.
    """

    def get_name(self) -> str:
        return "Bubble Sort"

    def get_steps(self, arr: List[int]) -> List[Tuple[str, List[int], str]]:
        """Generate animation steps for bubble sort."""
        steps = []
        arr_copy = arr.copy()
        n = len(arr_copy)

        for i in range(n):
            swapped = False

            for j in range(0, n - i - 1):
                # Compare adjacent elements
                steps.append(
                    (
                        "compare",
                        [j, j + 1],
                        f"Comparing {arr_copy[j]} and {arr_copy[j + 1]}",
                    )
                )

                if arr_copy[j] > arr_copy[j + 1]:
                    # Swap elements
                    steps.append(
                        (
                            "swap",
                            [j, j + 1],
                            f"Swapping {arr_copy[j]} and {arr_copy[j + 1]}",
                        )
                    )
                    arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
                    swapped = True

            # Mark the last element as sorted after each pass
            steps.append(
                (
                    "mark_sorted",
                    [n - i - 1],
                    f"Element {arr_copy[n - i - 1]} is now in correct position",
                )
            )

            # If no swapping occurred, the array is sorted
            if not swapped:
                # Mark all remaining elements as sorted
                for k in range(n - i - 1):
                    steps.append(
                        (
                            "mark_sorted",
                            [k],
                            f"Element {arr_copy[k]} is in correct position",
                        )
                    )
                break

        return steps

    def get_complexity(self) -> Tuple[str, str]:
        """Return time and space complexity."""
        return ("O(n²)", "O(1)")

    def get_description(self) -> str:
        """Return algorithm description."""
        return "Compares adjacent elements and swaps them if they are in wrong order. Repeats until no swaps are needed."
