import pytest
from repositorios.code_katas.src.minmax import maxi


# happy path: retorna o maior elemento para listas não vazias com variados números
@pytest.mark.parametrize("lst,expected", [
    ([1, 3, 2], 3),
    ([-5, -1, -3, -1], -1),
    ([1, 1, 1], 1),
    ([0, -10, 10], 10),
    ([2, 2.5, 2.5], 2.5),
])
def test_maxi_non_empty_lists(lst, expected):
    assert maxi(lst) == expected

# edge case: lista vazia deve retornar a própria lista
def test_maxi_empty_list_returns_empty():
    assert maxi([]) == []
