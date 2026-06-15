import pytest
from repositorios.code_katas.src.flight_graph import Graph

# teste: caminho feliz - verifica ordem de inserção dos nós
def test_nodes_happy_path_preserves_insertion_order():
    g = Graph()
    g.add_node("A")
    g.add_node("B")
    g.add_node("C")
    assert g.nodes() == ["A", "B", "C"]

# teste: caso vazio - retorna lista vazia
def test_nodes_empty_graph_returns_empty_list():
    g = Graph()
    assert g.nodes() == []
