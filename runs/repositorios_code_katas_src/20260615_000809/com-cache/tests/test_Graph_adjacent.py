import pytest
from repositorios.code_katas.src.flight_graph import Graph

# happy path: edge exists in one direction, returns True
def test_adjacent_true_edge_present():
    g = Graph()
    g.graph = {'A': {'B': 1}, 'B': {}}
    assert g.adjacent('A', 'B') is True

# branch: no edge between nodes, should return False
def test_adjacent_false_no_edge():
    g = Graph()
    g.graph = {'A': {'C': 5}, 'B': {}, 'C': {}, 'D': {}}
    assert g.adjacent('A', 'B') is False

# exception: node1 not in graph raises KeyError
def test_adjacent_raises_keyerror_node1_missing():
    g = Graph()
    g.graph = {'X': {'Y': 1}}
    with pytest.raises(KeyError):
        g.adjacent('A', 'X')

# exception: node2 not in graph raises KeyError
def test_adjacent_raises_keyerror_node2_missing():
    g = Graph()
    g.graph = {'A': {'B': 1}}
    with pytest.raises(KeyError):
        g.adjacent('A', 'C')
