import pytest
from repositorios.code_katas.src.sum_of_nth_terms import series_sum

# Verifica cenários variados (bordas e path): n=-3, 0, 1, 2 e 5
@pytest.mark.parametrize("n, expected", [
    (-3, "0.00"),
    (0, "0.00"),
    (1, "1.00"),
    (2, "1.25"),
    (5, "1.57"),
])
def test_series_sum_various_cases(n, expected):
    assert series_sum(n) == expected
