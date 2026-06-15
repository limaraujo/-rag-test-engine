import pytest
from repositorios.code_katas.src.sum_positive import positive_sum

# curto: happy path com números mistos; verifica soma de positivos
def test_positive_sum_happy_path():
    assert positive_sum([1, -2, 3, 0, 4]) == 8

# curto: entrada None deve retornar zero
def test_positive_sum_none_input():
    assert positive_sum(None) == 0

# curto: entrada vazia deve retornar zero
def test_positive_sum_empty_list():
    assert positive_sum([]) == 0

# curto: elementos não numéricos devem provocar TypeError
def test_positive_sum_type_error_on_non_numeric():
    with pytest.raises(TypeError):
        positive_sum([1, "a", 2])
