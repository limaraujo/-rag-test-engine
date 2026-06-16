import pytest
from repositorios.code_katas.src.minmax import mini

# Verifica que listas não vazias com números retornam o menor elemento (happy path)
@pytest.mark.parametrize("lst,expected", [
    ([3, 1, 2], 1),
    ([10, -1, 5], -1),
    ([7], 7),
])
def test_mini_finds_smallest_numbers(lst, expected):
    assert mini(lst) == expected

# Verifica que listas não vazias com strings retornam o menor elemento (strings comparáveis)
@pytest.mark.parametrize("lst,expected", [
    (["b", "a", "c"], "a"),
    (["apple", "banana", "apricot"], "apple"),
])
def test_mini_finds_smallest_strings(lst, expected):
    assert mini(lst) == expected

# Verifica que listas vazias retornam a própria lista (caso de borda)
def test_mini_empty_list_returns_input():
    assert mini([]) == []
