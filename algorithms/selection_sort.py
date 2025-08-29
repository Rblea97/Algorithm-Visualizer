from typing import List, Tuple
from .base_algorithm import SortingAlgorithm


class SelectionSort(SortingAlgorithm):
    """
    Selection Sort implementation with step-by-step animation support.

    Finds the minimum element from the unsorted portion and places it
    at the beginning of the unsorted portion.
    """

    def get_name(self) -> str:
        return "Selection Sort"

    def get_steps(self, arr: List[int]) -> List[Tuple[str, List[int], str]]:
        """Generate animation steps for selection sort."""
        steps = []
        arr_copy = arr.copy()
        n = len(arr_copy)

        for i in range(n):
            # Find minimum element in remaining unsorted array
            min_idx = i
            steps.append(
                ("highlight_current", [i], f"Finding minimum element from position {i}")
            )

            for j in range(i + 1, n):
                # Compare current element with minimum
                steps.append(
                    (
                        "compare",
                        [min_idx, j],
                        f"Comparing {arr_copy[min_idx]} with {arr_copy[j]}",
                    )
                )

                if arr_copy[j] < arr_copy[min_idx]:
                    min_idx = j
                    steps.append(
                        (
                            "highlight_min",
                            [min_idx],
                            f"New minimum found: {arr_copy[min_idx]} at position {min_idx}",
                        )
                    )

            # Swap the found minimum element with the first element
            if min_idx != i:
                steps.append(
                    (
                        "swap",
                        [i, min_idx],
                        f"Swapping {arr_copy[i]} with minimum {arr_copy[min_idx]}",
                    )
                )
                arr_copy[i], arr_copy[min_idx] = arr_copy[min_idx], arr_copy[i]

            # Mark current position as sorted
            steps.append(
                (
                    "mark_sorted",
                    [i],
                    f"Element {arr_copy[i]} is now in correct position",
                )
            )

        return steps

    def get_complexity(self) -> Tuple[str, str]:
        """Return time and space complexity."""
        return ("O(n²)", "O(1)")

    def get_description(self) -> str:
        """Return algorithm description."""
        return "Finds the minimum element from the unsorted portion and places it at the beginning."
