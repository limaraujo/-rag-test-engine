import pytest
from repositorios.code_katas.src.sum_of_nth_terms import series_sum

# Testa caminho principal (happy path) com n variados para verificar soma e formatação
@pytest.mark.parametrize("n,expected", [
    (1, "1.00"),
    (2, "1.25"),
    (3, "1.39"),
])
def test_series_sum_happy_path_multiple_n(n, expected):
    assert series_sum(n) == expected

# Testa casos de borda: n zero e n negativo resultando em soma zero
def test_series_sum_zero_and_negative_n():
    assert series_sum(0) == "0.00"
    assert series_sum(-5) == "0.00"
