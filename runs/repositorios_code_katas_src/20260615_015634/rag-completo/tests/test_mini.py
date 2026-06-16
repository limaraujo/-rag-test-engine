import pytest
from repositorios.code_katas.src.minmax import mini

# Teste de caminho feliz com várias entradas não vazias (min correto)
@pytest.mark.parametrize("lst, expected", [
    ([3, 1, 2], 1),
    ([5, 5, 1, 3], 1),
    ([-10, 0, 10, -5], -10),
    ([1], 1),
])
def test_mini_happy_path_various(lst, expected):
    assert mini(lst) == expected

# Teste do caminho falso para lista vazia (retorna a própria lista vazia)
def test_mini_empty_list_returns_empty_list():
    assert mini([]) == []
