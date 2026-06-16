import pytest
from repositorios.code_katas.src.flight_graph import Graph

# curto: happy path - edge A->B existe e é removido
def test_del_edge_happy_path():
    g = Graph()
    g.graph = {'A': {'B': 1}, 'B': {'A': 1}}
    g.del_edge('A', 'B')
    assert 'B' not in g.graph['A']

# curto: KeyError quando um dos nós não está no grafo (caminho elif)
def test_del_edge_missing_node_raises_keyerror():
    g = Graph()
    g.graph = {'A': {'B': 1}, 'B': {}}
    with pytest.raises(KeyError):
        g.del_edge('A', 'C')

# curto: ValueError quando a aresta não existe entre nós existentes (caminho else)
def test_del_edge_edge_not_in_graph_raises_valueerror():
    g = Graph()
    g.graph = {'A': {}, 'B': {'A': 1}}
    with pytest.raises(ValueError):
        g.del_edge('A', 'B')
