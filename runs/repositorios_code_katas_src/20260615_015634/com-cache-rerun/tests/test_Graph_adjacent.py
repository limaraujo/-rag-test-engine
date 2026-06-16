import pytest
from repositorios.code_katas.src.flight_graph import Graph

# curto: happy path - edge A-B exists; adjacent should be True in both directions
def test_adjacent_happy_path_bidirectional():
    g = Graph()
    g.add_edge("A", "B", weight=3)
    assert g.adjacent("A", "B") is True
    assert g.adjacent("B", "A") is True

# curto: edge ausente entre nós existentes - deve retornar False
def test_adjacent_false_when_no_edge_between_existing_nodes():
    g = Graph()
    g.add_edge("A", "B", weight=3)
    g.add_edge("C", "D", weight=2)
    assert g.adjacent("A", "C") is False

# curto: primeira chave ausente - deve levantar KeyError
def test_adjacent_raises_keyerror_for_missing_node1():
    g = Graph()
    g.add_edge("A", "B", weight=3)
    with pytest.raises(KeyError) as excinfo:
        g.adjacent("X", "A")
    assert "X is not in the graph." in str(excinfo.value)

# curto: segunda chave ausente - deve levantar KeyError
def test_adjacent_raises_keyerror_for_missing_node2():
    g = Graph()
    g.add_edge("A", "B", weight=3)
    with pytest.raises(KeyError) as excinfo:
        g.adjacent("A", "X")
    assert "X is not in the graph." in str(excinfo.value)
