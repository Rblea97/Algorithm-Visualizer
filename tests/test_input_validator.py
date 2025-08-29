"""
Unit tests for InputValidator class.

Tests cover security aspects including input sanitization,
malicious input handling, and edge case validation.
"""

import pytest
from utils.input_validator import InputValidator


class TestInputValidator:
    """Test cases for InputValidator security and robustness."""
    
    def test_valid_input(self):
        """Test valid comma-separated integers."""
        valid, numbers, error = InputValidator.validate_input("1,2,3,4,5")
        assert valid is True
        assert numbers == [1, 2, 3, 4, 5]
        assert error is None
    
    def test_empty_input(self):
        """Test empty input handling."""
        valid, numbers, error = InputValidator.validate_input("")
        assert valid is False
        assert numbers is None
        assert error is not None
    
    def test_whitespace_handling(self):
        """Test whitespace sanitization."""
        valid, numbers, error = InputValidator.validate_input("  1 , 2 , 3  ")
        assert valid is True
        assert numbers == [1, 2, 3]
    
    def test_trailing_comma(self):
        """Test trailing comma handling."""
        valid, numbers, error = InputValidator.validate_input("1,2,3,")
        assert valid is True
        assert numbers == [1, 2, 3]
    
    def test_double_commas(self):
        """Test double comma handling."""
        valid, numbers, error = InputValidator.validate_input("1,,2,3")
        assert valid is True
        assert numbers == [1, 2, 3]
    
    def test_negative_numbers(self):
        """Test negative number rejection (outside valid range 1-100)."""
        valid, numbers, error = InputValidator.validate_input("-5,-1,0,1,5")
        assert valid is False  # Negative numbers and zero are outside valid range
        assert numbers is None
        assert error is not None
    
    # Security Tests
    def test_sql_injection_attempt(self):
        """Test SQL injection-like input."""
        malicious_input = "1; DROP TABLE users; --"
        valid, numbers, error = InputValidator.validate_input(malicious_input)
        assert valid is False
        assert numbers is None
        assert error is not None
    
    def test_script_injection_attempt(self):
        """Test script injection-like input."""
        malicious_input = "<script>alert('xss')</script>"
        valid, numbers, error = InputValidator.validate_input(malicious_input)
        assert valid is False
        assert numbers is None
        assert error is not None
    
    def test_buffer_overflow_attempt(self):
        """Test extremely long input."""
        long_input = "1," * 1000  # Attempt to create very long input
        valid, numbers, error = InputValidator.validate_input(long_input)
        assert valid is False  # Should fail due to size limits
        assert numbers is None
        assert error is not None
    
    def test_invalid_characters(self):
        """Test input with invalid characters."""
        invalid_inputs = [
            "1,2,abc,4",
            "1.5,2.5,3.5",
            "1,2,3e4,5",
            "1,2,0xFF,4",
            "1,2,∞,4"
        ]
        
        for invalid_input in invalid_inputs:
            valid, numbers, error = InputValidator.validate_input(invalid_input)
            assert valid is False, f"Should reject: {invalid_input}"
            assert numbers is None
            assert error is not None
    
    def test_range_validation(self):
        """Test number range validation."""
        # Test values outside expected range
        valid, numbers, error = InputValidator.validate_input("999999")
        assert valid is False  # Assuming max value < 999999
        assert numbers is None
        assert error is not None
    
    def test_format_input(self):
        """Test input formatting function."""
        numbers = [1, 2, 3, 4, 5]
        formatted = InputValidator.format_input(numbers)
        assert formatted == "1, 2, 3, 4, 5"
    
    def test_array_size_validation(self):
        """Test array size limits."""
        # Test maximum size
        assert InputValidator.validate_array_size(50) is True
        assert InputValidator.validate_array_size(1000) is False
        assert InputValidator.validate_array_size(0) is False
    
    def test_validation_message(self):
        """Test validation message generation."""
        numbers = [1, 3, 5, 2, 4]
        message = InputValidator.get_validation_message(numbers)
        assert "5 elements" in message
        assert "1-5" in message or "range: 1-5" in message
    
    def test_regex_validation(self):
        """Test internal regex validation."""
        assert InputValidator._is_valid_integer("123") is True
        assert InputValidator._is_valid_integer("-123") is True
        assert InputValidator._is_valid_integer("abc") is False
        assert InputValidator._is_valid_integer("12.3") is False
        assert InputValidator._is_valid_integer("") is False
    
    # Edge Cases
    def test_single_element(self):
        """Test single element input."""
        valid, numbers, error = InputValidator.validate_input("42")
        assert valid is True
        assert numbers == [42]
        assert error is None
    
    def test_zero_value(self):
        """Test zero value rejection (outside valid range 1-100)."""
        valid, numbers, error = InputValidator.validate_input("0")
        assert valid is False  # Zero is outside valid range (1-100)
        assert numbers is None
        assert error is not None
    
    def test_valid_range_numbers(self):
        """Test valid numbers within range 1-100."""
        valid, numbers, error = InputValidator.validate_input("1,50,100")
        assert valid is True
        assert numbers == [1, 50, 100]
        assert error is None
    
    def test_duplicate_values(self):
        """Test duplicate values (should be allowed)."""
        valid, numbers, error = InputValidator.validate_input("1,1,2,2,3")
        assert valid is True
        assert numbers == [1, 1, 2, 2, 3]
        assert error is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])