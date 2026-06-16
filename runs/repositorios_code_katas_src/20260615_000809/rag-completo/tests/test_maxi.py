import pytest
from repositorios.code_katas.src.minmax import maxi

# Verifica caminho feliz: cenários com listas não vazias retornando o maior elemento (inclui números e strings)
@pytest.mark.parametrize("lst, expected", [
    ([1, 3, 2], 3),
    ([-1, -3, -2], -1),
    (["a", "c", "b"], "c"),
    ([7], 7),
])
def test_maxi_happy_path(lst, expected):
    assert maxi(lst) == expected

# Verifica caso de borda: lista vazia deve retornar a própria lista
def test_maxi_empty_list():
    assert maxi([]) == []
