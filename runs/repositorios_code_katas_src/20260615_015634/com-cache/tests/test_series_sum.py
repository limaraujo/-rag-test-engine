import pytest
from repositorios.code_katas.src.sum_of_nth_terms import series_sum

# Verifica caminho de borda: n = 0 retorna "0.00"
def test_series_sum_zero_path():
    assert series_sum(0) == "0.00"

# Verifica valores conhecidos para diferentes comprimentos da série
@pytest.mark.parametrize("n,expected", [
    (1, "1.00"),
    (2, "1.25"),
    (3, "1.39"),
    (4, "1.49"),
    (5, "1.57"),
])
def test_series_sum_known_values(n, expected):
    assert series_sum(n) == expected
