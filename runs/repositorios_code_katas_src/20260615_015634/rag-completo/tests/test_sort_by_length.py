import pytest
from repositorios.code_katas.src.sort_bylength import sort_by_length

# Verifica ordenação por comprimento em cenário comum (caminho feliz)
def test_sort_by_length_happy_path():
    arr = ["cat", "hi", "do", "a", "hello", "to", "be"]
    assert sort_by_length(arr) == ["a", "hi", "do", "to", "be", "cat", "hello"]

# Verifica comportamento com lista vazia (caso de borda)
def test_sort_by_length_empty_input():
    assert sort_by_length([]) == []

# Verifica preservação de ordem estável entre elementos com o mesmo comprimento
def test_sort_by_length_same_length_preserves_order():
    arr = ["ab", "cd", "ef"]
    assert sort_by_length(arr) == ["ab", "cd", "ef"]

# Verifica exceção ao encontrar elemento sem tamanho (TypeError esperado)
def test_sort_by_length_raises_on_non_sized_element():
    with pytest.raises(TypeError):
        sort_by_length([1, "a"])
