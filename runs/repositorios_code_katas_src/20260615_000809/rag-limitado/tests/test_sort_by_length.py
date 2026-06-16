import pytest
from repositorios.code_katas.src.sort_bylength import sort_by_length

# happy path: ordena por comprimento crescente
def test_sort_by_length_happy_path():
    input_list = ["a", "bb", "ccc", "dd"]
    expected = ["a", "bb", "dd", "ccc"]
    assert sort_by_length(input_list) == expected

# estabilidade com comprimentos iguais
def test_sort_by_length_stability_equal_lengths():
    input_list = ["apple", "bat", "cat", "doge"]
    expected = ["bat", "cat", "doge", "apple"]
    assert sort_by_length(input_list) == expected

# caso de borda: lista vazia
def test_sort_by_length_empty_input():
    assert sort_by_length([]) == []

# exceção: elementos não-string levantam TypeError
def test_sort_by_length_raises_typeerror_on_non_string_elements():
    with pytest.raises(TypeError):
        sort_by_length([1, "a"])
