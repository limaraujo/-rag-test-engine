import pytest
from repositorios.code_katas.src.minmax import maxi

# teste de caminho feliz: várias listas não vazias retornam o maior item
@pytest.mark.parametrize("lst, expected", [
    ([1, 3, 2], 3),
    ([5, 5, 1, 4], 5),
    ([-2, -5, -1], -1),
    ([0, -10, 10], 10),
    ([2, 2, 2], 2),
])
def test_maxi_happy_path(lst, expected):
    assert maxi(lst) == expected

# caso de borda: lista vazia deve retornar a própria lista vazia
def test_maxi_empty_list_returns_empty():
    assert maxi([]) == []
