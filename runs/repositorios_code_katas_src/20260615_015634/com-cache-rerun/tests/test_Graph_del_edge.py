import pytest
from repositorios.code_katas.src.flight_graph import Graph

# curto: happy path - remove edge A->B when B has outgoing edges (A->B exists, B->C exists)
def test_del_edge_happy_path_removes_existing_edge_when_target_has_outgoing_edges():
    g = Graph()
    g.add_node("A")
    g.add_node("B")
    g.add_node("C")
    g.add_edge("A", "B", weight=1)
    g.add_edge("B", "C", weight=1)  # ensures B's adjacency is non-empty
    g.del_edge("A", "B")
    assert "B" not in g.graph["A"]
    assert "C" in g.graph["B"]

# curto: exception KeyError - um dos nós não existe no grafo
def test_del_edge_raises_keyerror_when_node_missing():
    g = Graph()
    g.add_node("A")
    # "Z" does not exist in the graph
    with pytest.raises(KeyError):
        g.del_edge("A", "Z")

# curto: exception ValueError - ambos nós existem, mas a aresta A->B não está presente
def test_del_edge_raises_valueerror_when_edge_not_in_graph_both_nodes_exist():
    g = Graph()
    g.add_node("A")
    g.add_node("B")
    # A->B edge is not present
    with pytest.raises(ValueError):
        g.del_edge("A", "B")
