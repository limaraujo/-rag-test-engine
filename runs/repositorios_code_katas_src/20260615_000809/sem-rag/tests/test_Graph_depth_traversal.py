import pytest
from repositorios.code_katas.src.flight_graph import Graph

# curto
def test_depth_traversal_happy_path_chain():
    # verifica caminho principal (happy path) em cadeia simples A -> B -> C -> D
    g = Graph.__new__(Graph)
    g.graph = {'A': {'B': {}}, 'B': {'C': {}}, 'C': {'D': {}}, 'D': {}}
    result = Graph.depth_traversal(g, 'A')
    assert result == ['A', 'B', 'C', 'D']

# curto
def test_depth_traversal_happy_path_branching():
    # verifica caminho principal com ramificações A -> {B, C} e B -> D, C -> E
    g = Graph.__new__(Graph)
    g.graph = {'A': {'B': {}, 'C': {}}, 'B': {'D': {}}, 'C': {'E': {}}, 'D': {}, 'E': {}}
    result = Graph.depth_traversal(g, 'A')
    assert result == ['A', 'B', 'D', 'C', 'E']

# curto
def test_depth_traversal_missing_key_raises():
    # verifica exceção KeyError quando start não está no grafo
    g = Graph.__new__(Graph)
    g.graph = {'A': {'B': {}}}
    with pytest.raises(KeyError):
        Graph.depth_traversal(g, 'X')
