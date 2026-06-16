import pytest
from repositorios.code_katas.src.sort_bylength import sort_by_length

# Teste de caminho feliz: ordenação básica por comprimento
def test_sort_by_length_basic_happy_path():
    assert sort_by_length(["ccc", "a", "bb"]) == ["a", "bb", "ccc"]

# Teste de estabilidade com comprimentos iguais
def test_sort_by_length_stability_equal_lengths():
    assert sort_by_length(["zz", "aa", "c", "dd"]) == ["c", "zz", "aa", "dd"]

# Teste paramétrico: casos de borda (lista vazia e lista com um elemento)
@pytest.mark.parametrize('arr,expected', [([], []), (["a"], ["a"])])
def test_sort_by_length_edge_cases(arr, expected):
    assert sort_by_length(arr) == expected

# Teste de exceção para entradas não-string
def test_sort_by_length_raises_type_error_on_non_strings():
    with pytest.raises(TypeError):
        sort_by_length([1])
