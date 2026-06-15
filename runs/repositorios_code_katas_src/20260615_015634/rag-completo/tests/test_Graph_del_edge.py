import pytest
from repositorios.code_katas.src.flight_graph import Graph

# short: happy path - edge exists and node2 has its own outgoing edges
def test_del_edge_happy_path():
    g = Graph()
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    g.del_edge("A", "B")
    assert "B" not in g.graph["A"]
    assert "C" in g.graph["B"]

# short: missing node2 in graph raises KeyError
def test_del_edge_missing_node2_raises_KeyError():
    g = Graph()
    g.add_node("A")
    with pytest.raises(KeyError):
        g.del_edge("A", "B")

# short: edge not in graph (edge missing) raises ValueError
def test_del_edge_edge_not_in_graph_raises_ValueError():
    g = Graph()
    g.add_edge("A", "B")  # B exists but has no outgoing edges
    with pytest.raises(ValueError):
        g.del_edge("A", "B")

# short: missing node1 in graph raises KeyError
def test_del_edge_missing_node1_raises_KeyError():
    g = Graph()
    g.add_node("B")
    with pytest.raises(KeyError):
        g.del_edge("A", "B")
