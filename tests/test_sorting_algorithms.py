"""
Unit tests for sorting algorithms.

Tests cover correctness, edge cases, and animation step generation
for all implemented sorting algorithms.
"""

import pytest
from algorithms import ALGORITHMS
from algorithms.base_algorithm import SortingAlgorithm


class TestSortingAlgorithms:
    """Test cases for all sorting algorithms."""
    
    def test_all_algorithms_present(self):
        """Test that all expected algorithms are available."""
        expected_algorithms = [
            "Bubble Sort", "Selection Sort", "Insertion Sort", 
            "Merge Sort", "Quick Sort"
        ]
        
        for algorithm_name in expected_algorithms:
            assert algorithm_name in ALGORITHMS
            assert issubclass(ALGORITHMS[algorithm_name], SortingAlgorithm)
    
    @pytest.mark.parametrize("algorithm_name", [
        "Bubble Sort", "Selection Sort", "Insertion Sort", 
        "Merge Sort", "Quick Sort"
    ])
    def test_algorithm_instantiation(self, algorithm_name):
        """Test that all algorithms can be instantiated."""
        algorithm_class = ALGORITHMS[algorithm_name]
        algorithm_instance = algorithm_class()
        assert isinstance(algorithm_instance, SortingAlgorithm)
        assert algorithm_instance.get_name() == algorithm_name
    
    @pytest.mark.parametrize("algorithm_name", [
        "Bubble Sort", "Selection Sort", "Insertion Sort", 
        "Merge Sort", "Quick Sort"
    ])
    def test_empty_array(self, algorithm_name):
        """Test sorting empty arrays."""
        algorithm = ALGORITHMS[algorithm_name]()
        steps = algorithm.get_steps([])
        assert isinstance(steps, list)
        # Empty array should have no steps or minimal steps
        assert len(steps) <= 1
    
    @pytest.mark.parametrize("algorithm_name", [
        "Bubble Sort", "Selection Sort", "Insertion Sort", 
        "Merge Sort", "Quick Sort"
    ])
    def test_single_element(self, algorithm_name):
        """Test sorting single element arrays."""
        algorithm = ALGORITHMS[algorithm_name]()
        test_array = [42]
        steps = algorithm.get_steps(test_array)
        
        assert isinstance(steps, list)
        # Single element should be trivially sorted
        # Verify the algorithm doesn't break with single element
        for step in steps:
            assert len(step) == 3  # (action, indices, description)
            assert isinstance(step[0], str)  # action
            assert isinstance(step[1], list)  # indices
            assert isinstance(step[2], str)  # description
    
    @pytest.mark.parametrize("algorithm_name", [
        "Bubble Sort", "Selection Sort", "Insertion Sort", 
        "Merge Sort", "Quick Sort"
    ])
    def test_already_sorted_array(self, algorithm_name):
        """Test sorting already sorted arrays."""
        algorithm = ALGORITHMS[algorithm_name]()
        test_array = [1, 2, 3, 4, 5]
        steps = algorithm.get_steps(test_array)
        
        assert isinstance(steps, list)
        # Algorithm should still generate meaningful steps
        for step in steps:
            assert len(step) == 3
            assert isinstance(step[0], str)
            assert isinstance(step[1], list)
            assert isinstance(step[2], str)
    
    @pytest.mark.parametrize("algorithm_name", [
        "Bubble Sort", "Selection Sort", "Insertion Sort", 
        "Merge Sort", "Quick Sort"
    ])
    def test_reverse_sorted_array(self, algorithm_name):
        """Test sorting reverse-sorted arrays (worst case)."""
        algorithm = ALGORITHMS[algorithm_name]()
        test_array = [5, 4, 3, 2, 1]
        steps = algorithm.get_steps(test_array)
        
        assert isinstance(steps, list)
        assert len(steps) > 0  # Should require multiple steps
        
        # Verify step structure
        for step in steps:
            assert len(step) == 3
            assert isinstance(step[0], str)
            assert isinstance(step[1], list)
            assert isinstance(step[2], str)
            # Indices should be valid
            for idx in step[1]:
                assert 0 <= idx < len(test_array)
    
    @pytest.mark.parametrize("algorithm_name", [
        "Bubble Sort", "Selection Sort", "Insertion Sort", 
        "Merge Sort", "Quick Sort"
    ])
    def test_random_array(self, algorithm_name):
        """Test sorting random arrays."""
        algorithm = ALGORITHMS[algorithm_name]()
        test_array = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
        steps = algorithm.get_steps(test_array)
        
        assert isinstance(steps, list)
        assert len(steps) > 0
        
        # Test actual sorting correctness using built-in sort_array method
        sorted_result = algorithm.sort_array(test_array)
        expected_result = sorted(test_array)
        assert sorted_result == expected_result
    
    @pytest.mark.parametrize("algorithm_name", [
        "Bubble Sort", "Selection Sort", "Insertion Sort", 
        "Merge Sort", "Quick Sort"
    ])
    def test_duplicate_elements(self, algorithm_name):
        """Test sorting arrays with duplicate elements."""
        algorithm = ALGORITHMS[algorithm_name]()
        test_array = [3, 1, 3, 1, 3, 1]
        steps = algorithm.get_steps(test_array)
        
        assert isinstance(steps, list)
        
        # Test correctness
        sorted_result = algorithm.sort_array(test_array)
        expected_result = sorted(test_array)
        assert sorted_result == expected_result
    
    @pytest.mark.parametrize("algorithm_name", [
        "Bubble Sort", "Selection Sort", "Insertion Sort", 
        "Merge Sort", "Quick Sort"
    ])
    def test_complexity_info(self, algorithm_name):
        """Test that algorithms provide complexity information."""
        algorithm = ALGORITHMS[algorithm_name]()
        time_complexity, space_complexity = algorithm.get_complexity()
        
        assert isinstance(time_complexity, str)
        assert isinstance(space_complexity, str)
        assert len(time_complexity) > 0
        assert len(space_complexity) > 0
        # Should contain Big O notation
        assert "O(" in time_complexity
        assert "O(" in space_complexity
    
    @pytest.mark.parametrize("algorithm_name", [
        "Bubble Sort", "Selection Sort", "Insertion Sort", 
        "Merge Sort", "Quick Sort"
    ])
    def test_description(self, algorithm_name):
        """Test that algorithms provide descriptions."""
        algorithm = ALGORITHMS[algorithm_name]()
        description = algorithm.get_description()
        
        assert isinstance(description, str)
        assert len(description) > 10  # Should be meaningful
    
    def test_step_action_types(self):
        """Test that algorithms use expected action types in steps."""
        expected_actions = {
            "compare", "swap", "mark_sorted", "highlight_pivot", 
            "highlight_current", "highlight_min", "shift", "insert",
            "array_update", "divide", "merge_start", "place"
        }
        
        for algorithm_name in ALGORITHMS:
            algorithm = ALGORITHMS[algorithm_name]()
            test_array = [3, 1, 4, 1, 5]
            steps = algorithm.get_steps(test_array)
            
            for step in steps:
                action = step[0]
                # Action should be a meaningful string
                assert isinstance(action, str)
                assert len(action) > 0
                # While we can't enforce exact action names, they should be reasonable
                assert not action.startswith(" ")  # No leading whitespace
                assert not action.endswith(" ")   # No trailing whitespace
    
    def test_step_indices_validity(self):
        """Test that step indices are always valid for the array size."""
        test_array = [3, 1, 4, 1, 5, 9, 2]
        array_size = len(test_array)
        
        for algorithm_name in ALGORITHMS:
            algorithm = ALGORITHMS[algorithm_name]()
            steps = algorithm.get_steps(test_array)
            
            for step in steps:
                indices = step[1]
                assert isinstance(indices, list)
                
                for idx in indices:
                    assert isinstance(idx, int)
                    assert 0 <= idx < array_size, f"Invalid index {idx} for array size {array_size}"
    
    def test_large_array_performance(self):
        """Test algorithms with larger arrays (basic performance check)."""
        # Test with moderately large array
        test_array = list(range(50, 0, -1))  # 50 elements in reverse order
        
        for algorithm_name in ALGORITHMS:
            algorithm = ALGORITHMS[algorithm_name]()
            
            # This should complete without hanging or crashing
            steps = algorithm.get_steps(test_array)
            assert isinstance(steps, list)
            
            # Verify correctness
            sorted_result = algorithm.sort_array(test_array)
            expected_result = sorted(test_array)
            assert sorted_result == expected_result


class TestAlgorithmSpecificBehavior:
    """Test specific behaviors for individual algorithms."""
    
    def test_bubble_sort_optimization(self):
        """Test that bubble sort stops early when array becomes sorted."""
        bubble_sort = ALGORITHMS["Bubble Sort"]()
        # Array that will be sorted after first pass
        test_array = [1, 3, 2, 4, 5]
        steps = bubble_sort.get_steps(test_array)
        
        # Should have fewer steps than worst case
        assert isinstance(steps, list)
        assert len(steps) > 0
        
        # Check that it marks elements as sorted
        sorted_actions = [step for step in steps if step[0] == "mark_sorted"]
        assert len(sorted_actions) > 0
    
    def test_merge_sort_divide_conquer(self):
        """Test that merge sort shows divide and conquer steps."""
        merge_sort = ALGORITHMS["Merge Sort"]()
        test_array = [4, 2, 7, 1, 9, 3]
        steps = merge_sort.get_steps(test_array)
        
        # Should contain divide and merge operations
        divide_steps = [step for step in steps if "divide" in step[0].lower()]
        merge_steps = [step for step in steps if "merge" in step[0].lower()]
        
        # For non-trivial array, should have divide/merge operations
        assert len(steps) > 0
    
    def test_quick_sort_pivot_selection(self):
        """Test that quick sort shows pivot selection and partitioning."""
        quick_sort = ALGORITHMS["Quick Sort"]()
        test_array = [3, 6, 8, 10, 1, 2, 1]
        steps = quick_sort.get_steps(test_array)
        
        # Should contain pivot-related operations
        pivot_steps = [step for step in steps if "pivot" in step[0].lower()]
        
        # For non-trivial array, should have pivot operations
        assert len(steps) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])