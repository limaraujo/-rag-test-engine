import pytest
from repositorios.code_katas.src.monkey import monkey_count

# happy path: n=5 returns [1,2,3,4,5]
@pytest.mark.parametrize("n,expected", [(5, [1, 2, 3, 4, 5])])
def test_monkey_count_happy_path(n, expected):
    assert monkey_count(n) == expected

# boundary case: n=1 returns [1]
def test_monkey_count_boundary_single():
    assert monkey_count(1) == [1]

# non-positive: n=0 and n=-3 yield []
@pytest.mark.parametrize("n,expected", [(0, []), (-3, [])])
def test_monkey_count_non_positive(n, expected):
    assert monkey_count(n) == expected
