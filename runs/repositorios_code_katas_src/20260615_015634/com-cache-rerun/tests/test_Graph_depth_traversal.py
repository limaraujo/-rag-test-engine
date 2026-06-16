import pytest
from repositorios.code_katas.src.flight_graph import Graph

# curto: happy path - DFS em gráfico simples com árvore
def test_depth_traversal_happy_path_simple_tree():
    g = Graph()
    g.graph = {"A": {"B": {}, "C": {}}, "B": {"D": {}}, "C": {}, "D": {}}
    assert g.depth_traversal("A") == ["A", "B", "D", "C"]

# curto: exceção KeyError esperada quando start não está no grafo
def test_depth_traversal_missing_start_key_raises():
    g = Graph()
    g.graph = {"A": {}}
    with pytest.raises(KeyError) as excinfo:
        g.depth_traversal("B")
    assert "B not in graph." in str(excinfo.value)

# curto: grafo com ciclo não leva a recursão infinita
def test_depth_traversal_cycle_no_infinite_loop():
    g = Graph()
    g.graph = {"A": {"B": {}}, "B": {"A": {}}}
    assert g.depth_traversal("A") == ["A", "B"]

# curto: nó isolado retorna apenas ele
def test_depth_traversal_single_node():
    g = Graph()
    g.graph = {"A": {}}
    assert g.depth_traversal("A") == ["A"]
