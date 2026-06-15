import pytest
from repositorios.code_katas.src.sum_of_nth_terms import series_sum

# verifica comportamento com n=0 (caso de borda)
def test_series_sum_zero():
    assert series_sum(0) == "0.00"

# verifica soma para múltiplos n (happy path para n > 0)
@pytest.mark.parametrize("n, expected", [
    (1, "1.00"),
    (2, "1.25"),
    (3, "1.39"),
    (4, "1.49"),
])
def test_series_sum_positive_values(n, expected):
    assert series_sum(n) == expected
