import pytest
from repositorios.code_katas.src.flight_graph import Graph

# short: happy path - edge A-B exists; adjacent should be True in both directions
def test_adjacent_happy_path_bidirectional():
    g = Graph()
    g.add_edge("A", "B", weight=3)
    assert g.adjacent("A", "B") is True
    assert g.adjacent("B", "A") is True

# short: exception for missing node1
def test_adjacent_missing_node1_raises_keyerror():
    g = Graph()
    with pytest.raises(KeyError) as exc:
        g.adjacent("X", "Y")
    assert "X is not in the graph." in str(exc.value)

# short: exception for missing node2 when node1 exists
def test_adjacent_missing_node2_raises_keyerror():
    g = Graph()
    g.add_edge("A", "B", weight=1)
    with pytest.raises(KeyError) as exc:
        g.adjacent("A", "C")
    assert "C is not in the graph." in str(exc.value)

# short: existing nodes but no edge between them -> False
def test_adjacent_no_edge_returns_false():
    g = Graph()
    g.add_edge("A", "B", weight=1)
    g.graph["C"] = {}
    assert g.adjacent("A", "C") is False
