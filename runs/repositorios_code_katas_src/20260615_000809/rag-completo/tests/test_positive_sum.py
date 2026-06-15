import pytest
from repositorios.code_katas.src.sum_positive import positive_sum

# caminho principal (happy path): soma 1, 2 e 3 resultando em 6
def test_positive_sum_happy_path():
    assert positive_sum([1, 2, 3]) == 6

# cenário com positivos, negativos e zeros: soma apenas os positivos (2 + 4)
def test_positive_sum_with_negatives_and_zeros():
    assert positive_sum([0, -1, 2, -3, 4]) == 6

# sem positivos: apenas negativos/zero, retorno esperado 0
def test_positive_sum_all_negative_and_zero():
    assert positive_sum([-5, -1, 0]) == 0

# caso de borda: lista vazia retorna 0
def test_positive_sum_empty_list():
    assert positive_sum([]) == 0
