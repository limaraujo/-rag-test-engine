import pytest
from repositorios.code_katas.src.flight_graph import Graph

def _build_graph():
    g = Graph()
    g.graph = {'A': {'B': {}}, 'B': {'A': {}}, 'C': {}}
    return g

# Verifica caminho principal: aresta entre A e B existe (happy path) e funciona em ambas direções
def test_adjacent_happy_path_bidir_edges():
    g = _build_graph()
    assert g.adjacent('A', 'B') is True
    assert g.adjacent('B', 'A') is True

# Verifica caso em que ambas as nodes existem, mas não há aresta entre elas
def test_adjacent_existing_nodes_no_edge_returns_false():
    g = _build_graph()
    assert g.adjacent('A', 'C') is False

# Verifica exceção KeyError quando node1 não está no grafo
def test_adjacent_raises_keyerror_when_node1_missing():
    g = _build_graph()
    with pytest.raises(KeyError):
        g.adjacent('X', 'A')

# Verifica exceção KeyError quando node2 não está no grafo
def test_adjacent_raises_keyerror_when_node2_missing():
    g = _build_graph()
    with pytest.raises(KeyError):
        g.adjacent('A', 'X')
