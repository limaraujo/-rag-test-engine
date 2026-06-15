import pytest
from repositorios.code_katas.src.flight_graph import Graph

# curto: happy path - DFS simples com ramos A->{B,C} e B->{D} (cobre caminho principal)
def test_depth_traversal_happy_path():
    graph = {'A': {'B': 1, 'C': 1}, 'B': {'D': 1}, 'D': {}, 'C': {}}
    g = Graph.__new__(Graph)
    g.graph = graph
    assert g.depth_traversal('A') == ['A', 'B', 'D', 'C']

# curto: exceção - start não existe no grafo (KeyError)
def test_depth_traversal_missing_key_raises():
    graph = {'A': {}}
    g = Graph.__new__(Graph)
    g.graph = graph
    with pytest.raises(KeyError) as exc:
        g.depth_traversal('B')
    assert "not in graph" in str(exc.value)

# curto: detecção de ciclo - evita loop infinito com A <-> B
def test_depth_traversal_cycle_no_infinite_loop():
    graph = {'A': {'B': 1}, 'B': {'A': 1}}
    g = Graph.__new__(Graph)
    g.graph = graph
    assert g.depth_traversal('A') == ['A', 'B']

# curto: caso de borda - nó folha sem arestas retorna apenas o nó inicial
def test_depth_traversal_single_node_leaf():
    graph = {'A': {}}
    g = Graph.__new__(Graph)
    g.graph = graph
    assert g.depth_traversal('A') == ['A']
