"""A simple calculator module with some intentional bugs for testing."""


def add(a, b):
    """Add two numbers."""
    return a + b


def subtract(a, b):
    """Subtract b from a."""
    return a - b


def multiply(a, b):
    """Multiply two numbers."""
    result = 0
    for _ in range(abs(b)):
        result = add(result, a)
    return result if b >= 0 else -result


def divide(a, b):
    """Divide a by b."""
    # Bug: No check for division by zero
    return a / b


def power(base, exponent):
    """Calculate base raised to the power of exponent."""
    if isinstance(exponent, float):
        # For floating-point exponents, use built-in pow function
        return pow(base, exponent)

    if exponent == 0:
        return 1

    if exponent > 0:
        result = 1
        for _ in range(exponent):
            result = multiply(result, base)
        return result
    else:
        # Handle negative exponents
        positive_exponent = -exponent
        result = 1
        for _ in range(positive_exponent):
            result = multiply(result, base)
        return 1 / result


def factorial(n):
    """Calculate the factorial of n."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    return multiply(n, factorial(subtract(n, 1)))


def calculate_average(numbers):
    """Calculate the average of a list of numbers."""
    # Bug: No check for empty list
    total = 0
    for num in numbers:
        total = add(total, num)
    return divide(total, len(numbers))


def find_max(numbers):
    """Find the maximum number in a list."""
    if not numbers:
        raise ValueError("Cannot find maximum value in an empty list")

    max_val = numbers[0]
    for num in numbers[1:]:
        if num > max_val:
            max_val = num
    return max_val
