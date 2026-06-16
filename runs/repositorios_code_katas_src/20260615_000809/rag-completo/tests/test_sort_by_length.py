import pytest
from repositorios.code_katas.src.sort_bylength import sort_by_length

# Verifica caminho principal (happy path) com entradas diversas e ordem estável
@pytest.mark.parametrize("input_list, expected", [
    (["bb", "a", "ccc", "dd"], ["a", "bb", "dd", "ccc"]),
    (["yellow", "red", "blue", "green"], ["red", "blue", "green", "yellow"])
])
def test_sort_by_length_basic_and_stability(input_list, expected):
    assert sort_by_length(input_list) == expected

# Verifica caso de entrada vazia
def test_sort_by_length_empty_input():
    assert sort_by_length([]) == []

# Verifica exceção TypeError quando há elemento sem len (caso de borda)
def test_sort_by_length_raises_type_error_on_non_string():
    with pytest.raises(TypeError):
        sort_by_length(["a", 2, "bbb"])
