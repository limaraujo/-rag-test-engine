import pytest
from repositorios.code_katas.src.sum_highlow import sum_array

@pytest.mark.parametrize("arr,expected", [
    ([6, 2, 1, 8, 10], 16),
    ([1, 2, 3], 2),
    ([-1, -2, -3, -4, -5], -9),
    ([5, 5, 5, 5], 10),
])
def test_sum_array_happy_path(arr, expected):
    assert sum_array(arr) == expected

@pytest.mark.parametrize("arr", [
    [],
    [5],
])
def test_sum_array_insufficient_length(arr):
    assert sum_array(arr) == 0
