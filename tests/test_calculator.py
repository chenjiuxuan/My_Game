"""Tests for calculator module with intentional bugs."""

import pytest
from my_game.calculator import (
    add,
    subtract,
    multiply,
    divide,
    power,
    factorial,
    calculate_average,
    find_max,
)


class TestCalculator:
    """Test class for calculator functions."""

    # Test cases for add function (no intentional bugs)
    def test_add_positive_numbers(self):
        """Test addition of two positive numbers."""
        assert add(2, 3) == 5

    def test_add_negative_numbers(self):
        """Test addition of two negative numbers."""
        assert add(-2, -3) == -5

    def test_add_zero(self):
        """Test addition with zero."""
        assert add(0, 5) == 5
        assert add(5, 0) == 5
        assert add(0, 0) == 0

    # Test cases for subtract function (no intentional bugs)
    def test_subtract_positive_numbers(self):
        """Test subtraction of positive numbers."""
        assert subtract(5, 3) == 2

    def test_subtract_negative_numbers(self):
        """Test subtraction with negative numbers."""
        assert subtract(-5, -3) == -2

    def test_subtract_zero(self):
        """Test subtraction with zero."""
        assert subtract(5, 0) == 5
        assert subtract(0, 5) == -5

    # Test cases for multiply function (no intentional bugs)
    def test_multiply_positive_numbers(self):
        """Test multiplication of positive numbers."""
        assert multiply(2, 3) == 6

    def test_multiply_negative_numbers(self):
        """Test multiplication of negative numbers."""
        assert multiply(-2, -3) == 6
        assert multiply(-2, 3) == -6
        assert multiply(2, -3) == -6

    def test_multiply_by_zero(self):
        """Test multiplication by zero."""
        assert multiply(0, 5) == 0
        assert multiply(5, 0) == 0
        assert multiply(0, 0) == 0

    # Test cases for divide function (has bug: division by zero)
    def test_divide_positive_numbers(self):
        """Test division of positive numbers."""
        assert divide(6, 3) == 2

    def test_divide_negative_numbers(self):
        """Test division of negative numbers."""
        assert divide(-6, -3) == 2
        assert divide(-6, 3) == -2
        assert divide(6, -3) == -2

    def test_divide_by_zero(self):
        """Test division by zero - this should raise an exception (bug is no check)."""
        with pytest.raises(ZeroDivisionError):
            divide(5, 0)

    # Test cases for power function (has bug: negative exponents)
    def test_power_positive_exponent(self):
        """Test power with positive exponents."""
        assert power(2, 3) == 8
        assert power(5, 1) == 5

    def test_power_zero_exponent(self):
        """Test power with zero exponent."""
        assert power(5, 0) == 1
        assert power(0, 0) == 1  # Mathematically undefined, but code returns 1

    def test_power_negative_exponent(self):
        """Test power with negative exponents - this will fail (bug in implementation)."""
        assert power(2, -1) == 0.5
        assert power(4, -0.5) == 0.5

    def test_power_zero_base(self):
        """Test power with zero base."""
        assert power(0, 5) == 0
        assert power(0, 0) == 1

    # Test cases for factorial function (has bug: no negative number check)
    def test_factorial_positive_numbers(self):
        """Test factorial of positive numbers."""
        assert factorial(0) == 1
        assert factorial(1) == 1
        assert factorial(5) == 120

    def test_factorial_negative_number(self):
        """Test factorial of negative numbers - should raise exception (bug: no check)."""
        with pytest.raises(ValueError):
            factorial(-1)
        with pytest.raises(ValueError):
            factorial(-5)

    # Test cases for calculate_average function (has bug: empty list check)
    def test_calculate_average_positive_numbers(self):
        """Test average calculation with positive numbers."""
        assert calculate_average([1, 2, 3, 4, 5]) == 3

    def test_calculate_average_negative_numbers(self):
        """Test average calculation with negative numbers."""
        assert calculate_average([-1, -2, -3, -4, -5]) == -3

    def test_calculate_average_single_number(self):
        """Test average calculation with single number."""
        assert calculate_average([5]) == 5

    def test_calculate_average_empty_list(self):
        """Test average calculation with empty list - should raise exception (bug: no check)."""
        with pytest.raises(ZeroDivisionError):
            calculate_average([])

    # Test cases for find_max function (has bug: initial value and empty list)
    def test_find_max_positive_numbers(self):
        """Test find_max with positive numbers."""
        assert find_max([1, 3, 5, 2, 4]) == 5

    def test_find_max_negative_numbers(self):
        """Test find_max with negative numbers."""
        assert find_max([-1, -3, -5, -2, -4]) == -1

    def test_find_max_single_element(self):
        """Test find_max with single element list."""
        assert find_max([5]) == 5

    def test_find_max_empty_list(self):
        """Test find_max with empty list - should raise exception (bug: returns None)."""
        with pytest.raises(ValueError):
            find_max([])
