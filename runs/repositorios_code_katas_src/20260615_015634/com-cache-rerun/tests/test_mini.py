import pytest
from repositorios.code_katas.src.minmax import mini

# happy path: verifica que retorna o menor elemento para listas não vazias (casos diversos)
@pytest.mark.parametrize("lst, expected", [
    ([3, 1, 2], 1),
    ([-5, 0, 10, -3], -5),
    ([5], 5),
    ([2, 2, 2], 2),
])
def test_mini_happy_path(lst, expected):
    assert mini(lst) == expected

# branch: verifica que, em lista vazia, a função retorna a própria lista (empty branch)
def test_mini_empty_list_returns_same():
    assert mini([]) == []
