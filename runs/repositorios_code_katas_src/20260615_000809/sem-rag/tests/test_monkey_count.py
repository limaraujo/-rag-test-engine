import pytest
from repositorios.code_katas.src.monkey import monkey_count

# happy path: n=5 returns 1..5
def test_monkey_count_happy_path():
    assert monkey_count(5) == [1, 2, 3, 4, 5]

# edge case: n=0 returns empty list
def test_monkey_count_zero_returns_empty():
    assert monkey_count(0) == []

# edge case: negative n returns empty list
def test_monkey_count_negative_returns_empty():
    assert monkey_count(-3) == []

# exception: non-integer input raises TypeError
def test_monkey_count_non_integer_raises_type_error():
    with pytest.raises(TypeError):
        monkey_count(3.5)
