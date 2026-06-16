import pytest
from repositorios.code_katas.src.sum_of_nth_terms import series_sum

# Verifica a soma da série para diferentes valores de n (caminho feliz com casos simples)
@pytest.mark.parametrize("n, expected", [
    (0, "0.00"),
    (1, "1.00"),
    (2, "1.25"),
    (3, "1.39"),
])
def test_series_sum_various_n(n, expected):
    assert series_sum(n) == expected
