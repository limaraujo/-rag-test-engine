import pytest
from repositorios.code_katas.src.minmax import maxi

# Variações de listas não vazias (caminho feliz): números e strings devem retornar o maior item
@pytest.mark.parametrize("lst, expected", [
    ([1, 2, 3], 3),
    ([-5, -1, -10, 0], 0),
    (["apple", "orange", "banana"], "orange"),
    ([5, 5, 2, 7], 7),
])
def test_maxi_non_empty_lists(lst, expected):
    assert maxi(lst) == expected

# Caso de borda: lista vazia deve retornar a própria lista ([])
def test_maxi_empty_list_returns_empty_list():
    assert maxi([]) == []
