import pytest
from repositorios.code_katas.src.flight_graph import Graph

def _make_graph(dct):
    g = Graph.__new__(Graph)
    g.graph = dct
    return g

# happy path: edge exists and node2 has outgoing edges, edge is deleted
def test_del_edge_happy_path():
    g = _make_graph({'A': {'B': {}}, 'B': {'C': {'x': 1}}})
    g.del_edge('A', 'B')
    assert 'B' not in g.graph['A']

# border: node1 missing triggers KeyError
def test_del_edge_keyerror_node1_missing():
    g = _make_graph({'A': {'B': {}}, 'B': {'C': {}}})
    with pytest.raises(KeyError):
        g.del_edge('X', 'A')

# border: node2 missing triggers KeyError
def test_del_edge_keyerror_node2_missing():
    g = _make_graph({'A': {'B': {}}, 'B': {'C': {}}})
    with pytest.raises(KeyError):
        g.del_edge('A', 'X')

# invalid input scenario: nodes exist but edge does not exist -> ValueError
def test_del_edge_valueerror_edge_not_in_graph():
    g = _make_graph({'A': {'C': {}}, 'B': {'D': {}}})
    with pytest.raises(ValueError):
        g.del_edge('A', 'B')
