import pytest
from repositorios.code_katas.src.monkey import monkey_count

# Test positive inputs cover multiple valid results (1, 2, 5) via parametrization
@pytest.mark.parametrize("n,expected", [
    (1, [1]),
    (2, [1, 2]),
    (5, [1, 2, 3, 4, 5]),
])
def test_monkey_count_positive(n, expected):
    assert monkey_count(n) == expected

# Edge case: n=0 should yield empty list
def test_monkey_count_zero_returns_empty():
    assert monkey_count(0) == []

# Edge case: negative n should yield empty list (no negative numbers)
def test_monkey_count_negative_returns_empty():
    assert monkey_count(-3) == []
