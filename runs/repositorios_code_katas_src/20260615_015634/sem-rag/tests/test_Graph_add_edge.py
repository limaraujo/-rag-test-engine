import pytest
from repositorios.code_katas.src.flight_graph import Graph

# Teste: caminho feliz — ambos nós não existem; add_edge deve criar nós e a aresta
def test_add_edge_creates_both_nodes_and_edge_when_missing():
    g = Graph()
    g.add_edge("A", "B", weight=5)
    assert "A" in g.graph
    assert "B" in g.graph
    assert g.graph["A"]["B"] == 5

# Teste: apenas o nó de destino (node2) não existe; add_edge deve criar node2 e a aresta
def test_add_edge_creates_missing_target_node_when_only_node2_missing():
    g = Graph()
    g.add_node("A")  # node1 exists
    g.add_edge("A", "C", weight=7)
    assert "C" in g.graph
    assert g.graph["A"]["C"] == 7

# Teste: aresta já existente não é sobrescrita; o peso permanece
def test_add_edge_existing_edge_does_not_overwrite_weight():
    g = Graph()
    g.add_edge("X", "Y", weight=2)
    assert g.graph["X"]["Y"] == 2
    g.add_edge("X", "Y", weight=9)
    assert g.graph["X"]["Y"] == 2
