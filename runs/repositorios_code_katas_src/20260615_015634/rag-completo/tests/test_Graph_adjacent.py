import pytest
from repositorios.code_katas.src.flight_graph import Graph

# curto: happy path — edge exists between A and B
def test_adjacent_happy_path_edge_exists():
    g = Graph()
    g.graph = {'A': {'B': {}}, 'B': {}}
    assert g.adjacent('A', 'B') is True

# curto: case of no edge between existing nodes — should return False
def test_adjacent_no_edge_returns_false():
    g = Graph()
    g.graph = {'A': {'C': {}}, 'B': {'C': {}}}
    assert g.adjacent('A', 'B') is False

# curto: missing first node — should raise KeyError
def test_adjacent_missing_node1_raises():
    g = Graph()
    g.graph = {'A': {'B': {}}, 'B': {}}
    with pytest.raises(KeyError) as exc:
        g.adjacent('X', 'A')
    assert exc.value.args[0] == "X is not in the graph."

# curto: missing second node — should raise KeyError
def test_adjacent_missing_node2_raises():
    g = Graph()
    g.graph = {'A': {'B': {}}, 'B': {}}
    with pytest.raises(KeyError) as exc:
        g.adjacent('A', 'Y')
    assert exc.value.args[0] == "Y is not in the graph."
