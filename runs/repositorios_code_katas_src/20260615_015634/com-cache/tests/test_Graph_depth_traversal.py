import pytest
from repositorios.code_katas.src.flight_graph import Graph

# curto: happy path - nó isolado sem arestas retorna apenas o nó inicial
def test_depth_traversal_single_node():
    g = Graph()
    g.graph = {"A": {}}
    assert g.depth_traversal("A") == ["A"]

# curto: caminho em profundidade - grafo com várias arestas segue DFS com ordem de inserção
def test_depth_traversal_dfs_multiple_nodes():
    g = Graph()
    g.graph = {
        "A": {"B": {}, "C": {}},
        "B": {"D": {}},
        "D": {},
        "C": {"E": {}},
        "E": {}
    }
    assert g.depth_traversal("A") == ["A", "B", "D", "C", "E"]

# curto: exceção KeyError - start ausente lança erro com mensagem apropriada
def test_depth_traversal_missing_start_key():
    g = Graph()
    g.graph = {"X": {"Y": {}}}
    with pytest.raises(KeyError) as exc:
        g.depth_traversal("Z")
    assert "Z not in graph." in str(exc.value)

# curto: grafo com ciclo - evita recursion infinita e visita cada nó uma vez
def test_depth_traversal_with_cycle():
    g = Graph()
    g.graph = {
        "A": {"B": {}},
        "B": {"A": {}}
    }
    assert g.depth_traversal("A") == ["A", "B"]
