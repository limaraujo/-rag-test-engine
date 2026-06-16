import pytest
from repositorios.code_katas.src.flight_graph import Graph

# short: happy path - add a new node to an empty graph
def test_add_node_happy_path():
    g = Graph()
    g.add_node("A")
    assert "A" in g.graph
    assert g.graph["A"] == {}

# short: exception when adding a node that already exists in the graph
def test_add_node_existing_node_raises_keyerror():
    g = Graph()
    g.add_node("A")
    with pytest.raises(KeyError):
        g.add_node("A")

# short: border case where internal graph attribute is missing
def test_add_node_missing_graph_attribute_raises_attributeerror():
    g = Graph()
    delattr(g, "graph")
    with pytest.raises(AttributeError):
        g.add_node("B")
