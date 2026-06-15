import pytest
from repositorios.code_katas.src.flight_graph import Graph

# happy path: adding a new node inserts it with an empty adjacency dict
def test_add_node_happy_path():
    g = Graph()
    g.add_node("A")
    assert "A" in g.graph
    assert g.graph["A"] == {}

# edge case: adding a node that already exists raises KeyError
def test_add_node_duplicate_raises_KeyError():
    g = Graph()
    g.add_node("A")
    with pytest.raises(KeyError):
        g.add_node("A")

# multiple nodes: adding several nodes preserves existing ones and initializes new nodes
def test_add_node_multiple_nodes_preserves_existing():
    g = Graph()
    g.add_node("A")
    g.add_node("B")
    assert set(g.graph.keys()) == {"A", "B"}
    assert g.graph["A"] == {}
    assert g.graph["B"] == {}
