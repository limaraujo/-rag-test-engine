import pytest
from repositorios.code_katas.src.flight_graph import Graph

# curto: happy path - delete existing node with incoming edges and remove from neighbor lists
def test_del_node_happy_path_with_incoming_edges():
    g = Graph()
    g.add_node("A")
    g.add_node("B")
    g.add_node("C")
    # create edges A <-> B to exercise inner deletion branching
    g.graph["A"]["B"] = 1
    g.graph["B"]["A"] = 1
    g.del_node("A")
    assert "A" not in g.graph
    assert "A" not in g.graph.get("B", {})
    assert "B" in g.graph or "C" in g.graph  # other nodes remain

# curto: exception case - deleting a non-existent node raises KeyError
def test_del_node_missing_key_raises_keyerror():
    g = Graph()
    g.add_node("B")
    with pytest.raises(KeyError):
        g.del_node("A")

# curto: edge case - deleting the only node results in an empty graph
def test_del_node_last_node_results_in_empty_graph():
    g = Graph()
    g.add_node("A")
    g.del_node("A")
    assert g.graph == {}

# curto: case where no incoming edges exist - ensure other nodes remain untouched
def test_del_node_without_incoming_edges_keeps_others():
    g = Graph()
    g.add_node("A")
    g.add_node("B")
    # No edges to A from B
    g.del_node("A")
    assert "A" not in g.graph
    assert "B" in g.graph
    assert g.graph["B"] == {}
