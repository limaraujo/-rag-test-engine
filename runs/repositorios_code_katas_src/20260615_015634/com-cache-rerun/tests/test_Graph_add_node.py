import pytest
from repositorios.code_katas.src.flight_graph import Graph

# curto: happy path - inserir novo nó sem precedente
def test_add_node_happy_path():
    g = Graph()
    g.add_node("A")
    assert "A" in g.graph
    assert g.graph["A"] == {}

# curto: borda - tentar adicionar nó já existente levanta KeyError
def test_add_node_duplicate_raises():
    g = Graph()
    g.add_node("A")
    with pytest.raises(KeyError):
        g.add_node("A")

# curto: happy path - inserir múltiplos nós preservando a ordem
def test_add_multiple_nodes_insertion_order():
    g = Graph()
    g.add_node("A")
    g.add_node("B")
    assert list(g.graph.keys()) == ["A", "B"]
