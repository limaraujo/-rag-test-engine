import pytest
from repositorios.code_katas.src.flight_graph import Graph

# Verifica o caminho feliz: retorna vizinhos para nós presentes (multi-caso)
@pytest.mark.parametrize("node, expected", [
    ("A", ['B', 'C']),
    ("B", ['A']),
    ("C", ['A', 'D']),
])
def test_neighbors_happy_path(node, expected):
    g = Graph()
    g.graph = {
        'A': ['B', 'C'],
        'B': ['A'],
        'C': ['A', 'D']
    }
    assert g.neighbors(node) == expected

# missing_key: lança KeyError quando o nó não existe no grafo
def test_neighbors_missing_key_raises_keyerror():
    g = Graph()
    g.graph = {'A': []}
    with pytest.raises(KeyError):
        g.neighbors('B')
