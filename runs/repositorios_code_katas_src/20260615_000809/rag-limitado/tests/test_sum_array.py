import pytest
from repositorios.code_katas.src.sum_highlow import sum_array

# happy path: soma correta excluindo o menor e o maior valor
def test_sum_excludes_min_max_happy_path():
    assert sum_array([6, 2, 1, 8, 10]) == 16

# borda: cenários None, lista vazia, lista com 1 elemento e lista com 2 elementos devem retornar 0
@pytest.mark.parametrize("arr", [None, [], [5], [1, 2]])
def test_edge_cases_return_zero(arr):
    assert sum_array(arr) == 0

# duplicates: a soma deve considerar apenas os elementos intermediários após ordenação
def test_sum_with_duplicates():
    assert sum_array([1, 1, 2, 3, 3]) == 6

# negative numbers: verifica cálculo com números negativos
def test_sum_with_negative_numbers():
    assert sum_array([-4, -1, -2, -3]) == -5
