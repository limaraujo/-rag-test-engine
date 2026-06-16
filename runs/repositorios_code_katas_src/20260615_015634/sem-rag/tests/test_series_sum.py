import pytest
from repositorios.code_katas.src.sum_of_nth_terms import series_sum

# Verifica cenários válidos da série para diferentes n (happy path e caso de borda)
@pytest.mark.parametrize("n,expected", [
    (0, "0.00"),
    (1, "1.00"),
    (2, "1.25"),
    (5, "1.57"),
    (-1, "0.00"),
])
def test_series_sum_values(n, expected):
    assert series_sum(n) == expected

# Verifica que tipos inadequados de entrada levantam TypeError
def test_series_sum_invalid_type_raises_type_error():
    with pytest.raises(TypeError):
        series_sum(3.0)
