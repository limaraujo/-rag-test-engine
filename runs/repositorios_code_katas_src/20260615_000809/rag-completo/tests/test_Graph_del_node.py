import pytest
from repositorios.code_katas.src.flight_graph import Graph

# test: happy path - existing node deleted and incoming edges removed
def test_del_node_happy_path_removes_node_and_incoming_edges():
    g = Graph()
    g.graph = {
        'A': {'B': 1},
        'B': {'C': 2},
        'C': {}
    }
    g.del_node('B')
    assert 'B' not in g.graph
    assert g.graph['A'] == {}
    assert 'C' in g.graph

# test: missing node - should raise KeyError
def test_del_node_raises_when_node_missing():
    g = Graph()
    g.graph = {'A': {}}
    with pytest.raises(KeyError):
        g.del_node('B')

# test: existing node with no incoming edges - inner branch not taken
def test_del_node_no_incoming_edges_only():
    g = Graph()
    g.graph = {'A': {'C': 1}, 'B': {'D': 2}}
    g.del_node('B')
    assert 'B' not in g.graph
    assert g.graph == {'A': {'C': 1}}
