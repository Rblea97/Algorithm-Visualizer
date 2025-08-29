from typing import List, Tuple
from .base_algorithm import SortingAlgorithm


class InsertionSort(SortingAlgorithm):
    """
    Insertion Sort implementation with step-by-step animation support.

    Inserts each element into its correct position in the sorted portion
    of the array, similar to sorting playing cards in hand.
    """

    def get_name(self) -> str:
        return "Insertion Sort"

    def get_steps(self, arr: List[int]) -> List[Tuple[str, List[int], str]]:
        """Generate animation steps for insertion sort."""
        steps = []
        arr_copy = arr.copy()
        n = len(arr_copy)

        # Handle empty array
        if n == 0:
            return steps

        # First element is considered sorted
        steps.append(
            (
                "mark_sorted",
                [0],
                f"Element {arr_copy[0]} at position 0 is initially sorted",
            )
        )

        for i in range(1, n):
            key = arr_copy[i]
            steps.append(
                (
                    "highlight_current",
                    [i],
                    f"Inserting element {key} into sorted portion",
                )
            )

            j = i - 1

            # Move elements that are greater than key one position ahead
            while j >= 0 and arr_copy[j] > key:
                steps.append(("compare", [j, i], f"Comparing {arr_copy[j]} with {key}"))
                steps.append(
                    ("shift", [j, j + 1], f"Moving {arr_copy[j]} one position right")
                )

                arr_copy[j + 1] = arr_copy[j]
                j -= 1

            # Place key at its correct position
            if j + 1 != i:
                arr_copy[j + 1] = key
                steps.append(
                    (
                        "array_update",
                        list(range(len(arr_copy))),
                        f"Array updated: {arr_copy}",
                    )
                )
                steps.append(
                    ("insert", [j + 1], f"Inserting {key} at position {j + 1}")
                )

            # Mark the newly sorted portion
            for k in range(i + 1):
                if k <= i:
                    steps.append(
                        ("mark_sorted", [k], f"Position {k} is now in sorted portion")
                    )

        return steps

    def get_complexity(self) -> Tuple[str, str]:
        """Return time and space complexity."""
        return ("O(n²)", "O(1)")

    def get_description(self) -> str:
        """Return algorithm description."""
        return "Inserts each element into its correct position in the sorted portion of the array."
