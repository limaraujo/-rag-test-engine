import pytest
from repositorios.code_katas.src.flight_graph import Graph

# testando caminho feliz: edge existe e node2 possui adjacências (truthy)
def test_del_edge_happy_path():
    g = Graph()
    g.graph = {
        'A': {'B': 1},
        'B': {'C': 2},
        'C': {}
    }
    g.del_edge('A', 'B')
    assert 'B' not in g.graph['A']

# testando exceção KeyError quando um nó não existe no grafo
def test_del_edge_missing_node_raises_keyerror():
    g = Graph()
    g.graph = {
        'A': {'B': 1},
        'B': {'C': 2},
        'C': {}
    }
    with pytest.raises(KeyError):
        g.del_edge('X', 'A')

# testando exceção ValueError quando edge não existe entre node1 e node2
def test_del_edge_edge_not_in_graph_raises_valueerror():
    g = Graph()
    g.graph = {
        'A': {},
        'B': {'C': 1},
        'C': {}
    }
    with pytest.raises(ValueError):
        g.del_edge('A', 'B')
