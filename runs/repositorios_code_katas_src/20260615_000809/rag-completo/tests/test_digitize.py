import pytest
from repositorios.code_katas.src.convert import digitize

# Test: happy path with multi-digit positive number
def test_digitize_happy_path():
    assert digitize(35231) == [1, 3, 2, 5, 3]

# Test: edge case with zero
def test_digitize_zero():
    assert digitize(0) == [0]

# Test: edge case with a single-digit number
def test_digitize_single_digit():
    assert digitize(7) == [7]

# Test: negative input raises ValueError (handles invalid characters)
def test_digitize_negative_raises_value_error():
    with pytest.raises(ValueError):
        digitize(-123)
