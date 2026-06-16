import pytest
from repositorios.code_katas.src.flight_graph import Graph

# curto
def test_adjacent_happy_path_connected():
    g = Graph()
    g.graph = {'A': {'B': 1}, 'B': {}}
    assert g.adjacent('A', 'B') is True

# curto
def test_adjacent_missing_node1_raises_keyerror():
    g = Graph()
    g.graph = {'A': {}}
    with pytest.raises(KeyError) as excinfo:
        g.adjacent('X', 'A')
    assert excinfo.value.args[0] == "X is not in the graph."

# curto
def test_adjacent_missing_node2_raises_keyerror():
    g = Graph()
    g.graph = {'A': {}, 'B': {}}
    with pytest.raises(KeyError) as excinfo:
        g.adjacent('A', 'C')
    assert excinfo.value.args[0] == "C is not in the graph."

# curto
def test_adjacent_no_edge_returns_false():
    g = Graph()
    g.graph = {'A': {'C': 1}, 'B': {'D': 1}, 'C': {}}
    assert g.adjacent('A', 'B') is False
