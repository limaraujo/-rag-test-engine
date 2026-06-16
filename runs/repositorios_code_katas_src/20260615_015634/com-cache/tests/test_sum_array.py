import pytest
from repositorios.code_katas.src.sum_highlow import sum_array


# Verifica caminho feliz: lista com pelo menos 4 elementos distintos (min e max removidos)
def test_sum_array_happy_path_distinct():
    assert sum_array([1, 2, 3, 4]) == 5  # 2 + 3

# Verifica caminho feliz com duplicates: min/max removidos em presença de duplicatas
def test_sum_array_happy_path_with_duplicates():
    assert sum_array([1, 1, 2, 3, 4, 4]) == 10  # sum([1,2,3,4]) = 10

# Verifica caso de borda simples: apenas dois elementos
def test_sum_array_two_elements_returns_zero():
    assert sum_array([1, 2]) == 0

# Verifica casos de borda: lista vazia e lista com único elemento
@pytest.mark.parametrize("arr, expected", [
    ([], 0),
    ([5], 0),
])
def test_sum_array_zero_or_single(arr, expected):
    assert sum_array(arr) == expected
