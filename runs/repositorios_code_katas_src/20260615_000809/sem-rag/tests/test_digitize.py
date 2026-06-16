import pytest
from repositorios.code_katas.src.convert import digitize

# happy path: various non-negative integers including edge 0
@pytest.mark.parametrize("n,expected", [
    (0, [0]),
    (1, [1]),
    (12, [2, 1]),
    (305, [5, 0, 3]),
    (12345, [5, 4, 3, 2, 1]),
])
def test_digitize_happy_path(n, expected):
    assert digitize(n) == expected

# edge case: negative input raises ValueError
def test_digitize_negative_raises():
    with pytest.raises(ValueError):
        digitize(-123)
