import pytest
from repositorios.code_katas.src.convert import digitize

# happy path: normal multi-digit number to reversed digits
def test_digitize_happy_path():
    assert digitize(35231) == [1, 3, 2, 5, 3]

# edge: zero and single-digit
def test_digitize_zero_and_single_digit():
    assert digitize(0) == [0]
    assert digitize(7) == [7]

# large number: more digits
def test_digitize_large_number():
    assert digitize(123456) == [6, 5, 4, 3, 2, 1]

# error: negative input raises
def test_digitize_negative_raises():
    with pytest.raises(ValueError):
        digitize(-123)
