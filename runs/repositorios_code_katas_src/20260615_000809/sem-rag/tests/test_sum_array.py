import pytest
from repositorios.code_katas.src.sum_highlow import sum_array

# teste feliz: três números, removendo min e max
def test_sum_array_happy_three():
    assert sum_array([1, 2, 3]) == 2

# teste borda: dois números -> 0
def test_sum_array_two_elements_zero():
    assert sum_array([5, 7]) == 0

# teste com valores repetidos e negativos: verifica soma dos elementos do meio
def test_sum_array_duplicates_negatives():
    assert sum_array([-3, -1, -1, 2, 2]) == 0

# teste ramo falso: entradas vazias, nulas ou de tamanho 1 devem retornar 0
@pytest.mark.parametrize("arr, expected", [
    (None, 0),
    ([], 0),
    ([5], 0),
])
def test_sum_array_false_branch(arr, expected):
    assert sum_array(arr) == expected
