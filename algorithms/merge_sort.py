from typing import List, Tuple
from .base_algorithm import SortingAlgorithm


class MergeSort(SortingAlgorithm):
    """
    Merge Sort implementation with step-by-step animation support.

    Divides array into halves, sorts them recursively, then merges
    the sorted halves back together.
    """

    def get_name(self) -> str:
        return "Merge Sort"

    def get_steps(self, arr: List[int]) -> List[Tuple[str, List[int], str]]:
        """Generate animation steps for merge sort."""
        steps = []
        arr_copy = arr.copy()

        def merge_sort_helper(left: int, right: int):
            if left >= right:
                # Base case: single element or empty, mark as sorted
                if left == right:
                    steps.append(
                        (
                            "mark_sorted",
                            [left],
                            f"Single element {arr_copy[left]} is already sorted",
                        )
                    )
                return

            if left < right:
                mid = (left + right) // 2

                # Divide phase
                steps.append(
                    (
                        "divide",
                        [left, mid, right],
                        f"Dividing array from {left} to {right} at position {mid}",
                    )
                )

                # Recursively sort both halves
                merge_sort_helper(left, mid)
                merge_sort_helper(mid + 1, right)

                # Merge phase
                merge(left, mid, right)

        def merge(left: int, mid: int, right: int):
            # Create temporary arrays for left and right subarrays
            left_arr = arr_copy[left : mid + 1]
            right_arr = arr_copy[mid + 1 : right + 1]

            steps.append(
                (
                    "merge_start",
                    [left, mid, right],
                    f"Merging sorted subarrays [{left}..{mid}] and [{mid + 1}..{right}]",
                )
            )

            i = j = 0
            k = left

            # Merge the temporary arrays back into arr_copy[left..right]
            while i < len(left_arr) and j < len(right_arr):
                steps.append(
                    (
                        "compare",
                        [left + i, mid + 1 + j],
                        f"Comparing {left_arr[i]} and {right_arr[j]}",
                    )
                )

                if left_arr[i] <= right_arr[j]:
                    arr_copy[k] = left_arr[i]
                    steps.append(
                        ("place", [k], f"Placing {left_arr[i]} at position {k}")
                    )
                    i += 1
                else:
                    arr_copy[k] = right_arr[j]
                    steps.append(
                        ("place", [k], f"Placing {right_arr[j]} at position {k}")
                    )
                    j += 1
                k += 1

            # Copy remaining elements of left_arr, if any
            while i < len(left_arr):
                arr_copy[k] = left_arr[i]
                steps.append(
                    ("place", [k], f"Placing remaining {left_arr[i]} at position {k}")
                )
                i += 1
                k += 1

            # Copy remaining elements of right_arr, if any
            while j < len(right_arr):
                arr_copy[k] = right_arr[j]
                steps.append(
                    ("place", [k], f"Placing remaining {right_arr[j]} at position {k}")
                )
                j += 1
                k += 1

            # Update array state after merge
            steps.append(
                (
                    "array_update",
                    list(range(len(arr_copy))),
                    f"Array updated: {arr_copy}",
                )
            )

            # Mark merged section as sorted
            steps.append(
                (
                    "mark_sorted",
                    list(range(left, right + 1)),
                    f"Merged section [{left}..{right}] is now sorted",
                )
            )

        merge_sort_helper(0, len(arr_copy) - 1)
        return steps

    def get_complexity(self) -> Tuple[str, str]:
        """Return time and space complexity."""
        return ("O(n log n)", "O(n)")

    def get_description(self) -> str:
        """Return algorithm description."""
        return "Divides array into halves, sorts them recursively, then merges the sorted halves back together."
