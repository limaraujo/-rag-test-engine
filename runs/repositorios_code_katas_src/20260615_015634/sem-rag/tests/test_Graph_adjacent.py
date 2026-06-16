import pytest
from repositorios.code_katas.src.flight_graph import Graph

# helper to create a Graph-like instance without invoking __init__
def make_graph_with(adj_dict):
    g = Graph.__new__(Graph)
    g.graph = adj_dict
    return g

# curto: missing node1 raises KeyError
def test_adjacent_raises_when_node1_missing():
    g = make_graph_with({'A': {'B': 1}})
    with pytest.raises(KeyError) as exc:
        g.adjacent('X', 'A')
    assert exc.value.args[0] == "X is not in the graph."

# curto: missing node2 raises KeyError
def test_adjacent_raises_when_node2_missing():
    g = make_graph_with({'A': {'B': 1}})
    with pytest.raises(KeyError) as exc:
        g.adjacent('A', 'Y')
    assert exc.value.args[0] == "Y is not in the graph."

# curto: happy path where edge exists
def test_adjacent_true_when_edge_exists():
    g = make_graph_with({'A': {'B': 1}, 'B': {'A': 1}})
    assert g.adjacent('A', 'B') is True

# curto: edge does not exist between existing nodes
def test_adjacent_false_when_no_edge():
    g = make_graph_with({'A': {'C': 1}, 'B': {'D': 1}})
    assert g.adjacent('A', 'B') is False
