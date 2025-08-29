from abc import ABC, abstractmethod
from typing import List, Tuple


class SortingAlgorithm(ABC):
    """
    Abstract base class for sorting algorithms.

    Each algorithm must implement methods to generate animation steps,
    provide complexity information, and give a description.
    """

    @abstractmethod
    def get_steps(self, arr: List[int]) -> List[Tuple[str, List[int], str]]:
        """
        Generate animation steps for sorting the given array.

        Args:
            arr: List of integers to sort

        Returns:
            List of tuples in format (action, indices, description) where:
            - action: 'compare', 'swap', 'mark_sorted', 'highlight_pivot', etc.
            - indices: List of array indices involved in the action
            - description: Human-readable description of the current step
        """
        pass

    @abstractmethod
    def get_complexity(self) -> Tuple[str, str]:
        """
        Get the time and space complexity of the algorithm.

        Returns:
            Tuple of (time_complexity, space_complexity) as strings
        """
        pass

    @abstractmethod
    def get_description(self) -> str:
        """
        Get a brief description of how the algorithm works.

        Returns:
            String description of the algorithm
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """
        Get the name of the algorithm.

        Returns:
            String name of the algorithm
        """
        pass

    def sort_array(self, arr: List[int]) -> List[int]:
        """
        Actually sort the array (for validation purposes).
        Default implementation uses Python's built-in sort.

        Args:
            arr: List of integers to sort

        Returns:
            Sorted copy of the array
        """
        return sorted(arr)
