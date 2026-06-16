import pytest
from repositorios.code_katas.src.sum_of_nth_terms import series_sum

# verifica a soma da série para múltiplos valores de n (caso happy path, borda) com parametrização
@pytest.mark.parametrize("n, expected", [
    (0, "0.00"),
    (1, "1.00"),
    (2, "1.25"),
    (5, "1.57"),
])
def test_series_sum_various_n(n, expected):
    assert series_sum(n) == expected
