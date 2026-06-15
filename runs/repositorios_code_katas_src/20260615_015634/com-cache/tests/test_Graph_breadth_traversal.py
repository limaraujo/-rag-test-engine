import pytest
from repositorios.code_katas.src.flight_graph import Graph

# curto: happy path - BFS básico com árvore simples
def test_breadth_traversal_basic():
    g = Graph()
    g.graph = {"A": {"B": {}, "C": {}}, "B": {"D": {}}, "C": {}, "D": {}}
    assert g.breadth_traversal("A") == ["A", "B", "C", "D"]

# curto: branch - evitar duplicatas no traversal
def test_breadth_traversal_no_duplicates():
    g = Graph()
    g.graph = {"A": {"B": {}, "C": {}}, "B": {"C": {}}, "C": {}}
    assert g.breadth_traversal("A") == ["A", "B", "C"]

# curto: exceção quando o início não está no grafo
def test_breadth_traversal_start_not_in_graph_raises_keyerror():
    g = Graph()
    g.graph = {"A": {"B": {}}}
    with pytest.raises(KeyError):
        g.breadth_traversal("X")
