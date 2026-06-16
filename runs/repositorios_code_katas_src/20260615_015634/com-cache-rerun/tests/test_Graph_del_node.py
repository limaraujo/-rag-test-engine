import pytest
from repositorios.code_katas.src.flight_graph import Graph

# curto: happy path - delete existing node with an inbound edge from B
def test_del_node_happy_path_with_inbound_edge():
    g = Graph()
    g.add_node("A")
    g.add_node("B")
    g.add_edge("A", "B", weight=1)
    g.del_node("A")
    assert "A" not in g.graph
    assert "A" not in g.graph["B"]

# curto: exception - deleting non-existent node raises KeyError
def test_del_node_missing_key_raises():
    g = Graph()
    g.add_node("A")
    with pytest.raises(KeyError):
        g.del_node("B")

# curto: branch - delete node with multiple inbound edges from B and C
def test_del_node_removes_multiple_inbound_edges():
    g = Graph()
    g.add_node("A")
    g.add_node("B")
    g.add_node("C")
    g.add_edge("A", "B", weight=1)
    g.add_edge("A", "C", weight=2)
    g.del_node("A")
    assert "A" not in g.graph
    assert "A" not in g.graph["B"]
    assert "A" not in g.graph["C"]
