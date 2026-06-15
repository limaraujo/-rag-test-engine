import pytest
from repositorios.code_katas.src.flight_graph import Graph

# happy path: edge exists and is deleted
def test_del_edge_happy_path():
    g = Graph()
    g.graph = {'A': {'B': 1}, 'B': {'A': 2}}
    g.del_edge('A', 'B')
    assert 'B' not in g.graph['A']

# missing_key: one of the nodes does not exist in the graph
def test_del_edge_missing_key_raises():
    g = Graph()
    g.graph = {'A': {}}
    with pytest.raises(KeyError):
        g.del_edge('C', 'A')

# edge_not_in_graph: nodes exist but the edge does not exist (or second node's adjacency is empty)
def test_del_edge_edge_not_in_graph_raises():
    g = Graph()
    g.graph = {'A': {'B': 1}, 'B': {}}
    with pytest.raises(ValueError):
        g.del_edge('A', 'B')
