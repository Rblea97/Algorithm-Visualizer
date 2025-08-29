import re
from typing import List, Optional, Tuple
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.constants import VALUE_MIN, VALUE_MAX, ARRAY_SIZE_MAX, ERROR_MESSAGES


class InputValidator:
    """
    Handles validation of user input for the sorting visualizer.

    Validates comma-separated integers within specified range and count limits.
    """

    @staticmethod
    def validate_input(
        input_text: str,
    ) -> Tuple[bool, Optional[List[int]], Optional[str]]:
        """
        Validate user input string and convert to integer list.

        Args:
            input_text: Raw input string from user

        Returns:
            Tuple of (is_valid, parsed_numbers, error_message)
            - is_valid: True if input is valid
            - parsed_numbers: List of integers if valid, None if invalid
            - error_message: Error description if invalid, None if valid
        """

        # Remove whitespace and check for empty input
        input_text = input_text.strip()
        if not input_text:
            return False, None, ERROR_MESSAGES["EMPTY_INPUT"]

        # Remove trailing comma if present
        if input_text.endswith(","):
            input_text = input_text[:-1]

        # Split by comma and clean each part
        parts = [part.strip() for part in input_text.split(",")]

        # Remove empty parts (handles double commas, etc.)
        parts = [part for part in parts if part]

        if not parts:
            return False, None, ERROR_MESSAGES["EMPTY_INPUT"]

        # Check number of elements
        if len(parts) > ARRAY_SIZE_MAX:
            return False, None, ERROR_MESSAGES["TOO_MANY_ELEMENTS"]

        numbers = []

        for part in parts:
            # Check if part is a valid integer
            if not InputValidator._is_valid_integer(part):
                return False, None, ERROR_MESSAGES["INVALID_NUMBER"]

            try:
                num = int(part)

                # Check range
                if num < VALUE_MIN or num > VALUE_MAX:
                    return False, None, ERROR_MESSAGES["OUT_OF_RANGE"]

                numbers.append(num)

            except ValueError:
                return False, None, ERROR_MESSAGES["INVALID_NUMBER"]

        return True, numbers, None

    @staticmethod
    def _is_valid_integer(text: str) -> bool:
        """
        Check if a string represents a valid integer.

        Args:
            text: String to check

        Returns:
            True if text is a valid integer format
        """
        # Allow optional minus sign followed by digits
        pattern = r"^-?\d+$"
        return bool(re.match(pattern, text))

    @staticmethod
    def format_input(numbers: List[int]) -> str:
        """
        Format a list of numbers back to input string format.

        Args:
            numbers: List of integers

        Returns:
            Comma-separated string representation
        """
        return ", ".join(map(str, numbers))

    @staticmethod
    def validate_array_size(size: int) -> bool:
        """
        Validate if array size is within acceptable range.

        Args:
            size: Proposed array size

        Returns:
            True if size is valid
        """
        from .constants import ARRAY_SIZE_MIN, ARRAY_SIZE_MAX

        return ARRAY_SIZE_MIN <= size <= ARRAY_SIZE_MAX

    @staticmethod
    def get_validation_message(numbers: List[int]) -> str:
        """
        Get a descriptive message about the validated input.

        Args:
            numbers: List of validated numbers

        Returns:
            Descriptive message about the input
        """
        count = len(numbers)
        min_val = min(numbers)
        max_val = max(numbers)

        return f"Array of {count} elements (range: {min_val}-{max_val})"
