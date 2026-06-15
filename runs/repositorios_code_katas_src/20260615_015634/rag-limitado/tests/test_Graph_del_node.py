import pytest
from repositorios.code_katas.src.flight_graph import Graph

# happy path: remove an existing node and ensure it's removed from graph and from neighbors
def test_del_node_happy_path_removes_node_and_edges():
    g = Graph()
    g.graph = {
        'A': {'B': 1, 'C': 2},
        'B': {'A': 1},
        'C': {'A': 2}
    }

    g.del_node('B')

    assert 'B' not in g.graph
    assert g.graph['A'] == {'C': 2}
    assert g.graph['C'] == {'A': 2}

# exception path: attempting to delete a node that does not exist should raise KeyError
def test_del_node_raises_KeyError_when_missing():
    g = Graph()
    g.graph = {
        'A': {'B': 1},
        'B': {'A': 1}
    }

    with pytest.raises(KeyError):
        g.del_node('D')

# border/edge: deleting an isolated node should not modify other nodes' edges
def test_del_node_isolated_node_no_side_effects():
    g = Graph()
    g.graph = {
        'A': {'C': 5},
        'B': {},
        'C': {'A': 5}
    }

    g.del_node('B')

    assert 'B' not in g.graph
    assert g.graph['A'] == {'C': 5}
    assert g.graph['C'] == {'A': 5}
