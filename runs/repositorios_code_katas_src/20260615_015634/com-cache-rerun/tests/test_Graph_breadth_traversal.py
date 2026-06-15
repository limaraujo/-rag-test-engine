import pytest
from repositorios.code_katas.src.flight_graph import Graph

# curto: happy path - BFS básico com árvore simples
def test_breadth_traversal_basic_happy_path():
    g = Graph()
    g.graph = {"A": {"B": {}, "C": {}}, "B": {"D": {}}, "C": {}, "D": {}}
    assert g.breadth_traversal("A") == ["A", "B", "C", "D"]

# curto: happy path com ramificações - ordem BFS esperada
def test_breadth_traversal_order_with_branching():
    g = Graph()
    g.graph = {
        "A": {"B": {}, "C": {}},
        "B": {"E": {}, "F": {}},
        "C": {"G": {}},
        "E": {}, "F": {}, "G": {}
    }
    assert g.breadth_traversal("A") == ["A", "B", "C", "E", "F", "G"]

# curto: trata ciclo - evita repetição e loop infinito
def test_breadth_traversal_handles_cycle_no_infinite_loop():
    g = Graph()
    g.graph = {"A": {"B": {}, "C": {}}, "B": {"A": {}}, "C": {}}
    assert g.breadth_traversal("A") == ["A", "B", "C"]

# curto: erro quando início não está no grafo - KeyError
def test_breadth_traversal_key_error_on_missing_start():
    g = Graph()
    g.graph = {"A": {"B": {}, "C": {}}, "B": {}, "C": {}}
    with pytest.raises(KeyError):
        g.breadth_traversal("X")
