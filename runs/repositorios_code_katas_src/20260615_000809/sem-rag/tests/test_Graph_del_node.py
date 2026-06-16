import pytest
from repositorios.code_katas.src.flight_graph import Graph

# happy path: remove existing node and clean up all edges referencing it
def test_del_node_happy_path_removes_node_and_edges():
    g = Graph()
    g.graph = {
        "A": {"B": 1, "D": 1},
        "B": {"A": 1, "C": 1},
        "C": {"B": 1},
        "D": {"A": 1}
    }
    g.del_node("A")
    assert "A" not in g.graph
    assert "A" not in g.graph["B"]
    assert "A" not in g.graph["D"]
    # ensure other edges remain
    assert g.graph["B"] == {"C": 1}
    assert g.graph["C"] == {"B": 1}

# key error: attempting to delete a node that does not exist
def test_del_node_missing_key_raises_keyerror():
    g = Graph()
    g.graph = {"X": {"Y": 1}, "Y": {"X": 1}}
    with pytest.raises(KeyError):
        g.del_node("Z")

# inner branch coverage: node appears in some neighbor dicts, removed from all
def test_del_node_removes_incoming_edges_from_multiple_nodes():
    g = Graph()
    g.graph = {
        "A": {"B": 1, "D": 1},
        "B": {"A": 1, "C": 1},
        "C": {"B": 1},
        "D": {"A": 1, "E": 1}
    }
    g.del_node("A")
    assert "A" not in g.graph
    assert "A" not in g.graph["B"]
    assert "A" not in g.graph["D"]

# border: deleting a node with no incoming edges and no outgoing edges
def test_del_node_on_isolated_node():
    g = Graph()
    g.graph = {
        "A": {},
        "B": {"A": 1}
    }
    g.del_node("A")
    assert "A" not in g.graph
    assert g.graph["B"] == {}
