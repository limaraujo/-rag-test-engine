import pytest
from repositorios.code_katas.src.monkey import monkey_count

# short: happy path for positive small n values
@pytest.mark.parametrize("n,expected", [
    (5, [1, 2, 3, 4, 5]),
    (1, [1]),
])
def test_monkey_count_basic(n, expected):
    assert monkey_count(n) == expected

# short: large n to verify scalability of main path
def test_monkey_count_large_n():
    n = 100
    assert monkey_count(n) == list(range(1, n + 1))

# short: edge cases: n=0 and negative numbers produce empty list
@pytest.mark.parametrize("n,expected", [
    (0, []),
    (-3, []),
])
def test_monkey_count_zero_and_negative(n, expected):
    assert monkey_count(n) == expected

# short: invalid input types raise TypeError
@pytest.mark.parametrize("n", [3.0, "5"])
def test_monkey_count_invalid_type(n):
    with pytest.raises(TypeError):
        monkey_count(n)
