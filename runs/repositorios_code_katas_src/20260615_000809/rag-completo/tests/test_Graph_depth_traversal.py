import pytest
from repositorios.code_katas.src.flight_graph import Graph

def _make_graph(graph_dict):
    g = Graph.__new__(Graph)
    g.graph = graph_dict
    return g

# Teste de caminho feliz (happy path): DFS de A visitando B, D e depois C
def test_depth_traversal_happy_path():
    graph = {'A': {'B': {}, 'C': {}}, 'B': {'D': {}}, 'D': {}, 'C': {}}
    g = _make_graph(graph)
    assert g.depth_traversal('A') == ['A', 'B', 'D', 'C']

# Teste lança KeyError quando o início não está no grafo
def test_depth_traversal_missing_key():
    graph = {'A': {'B': {}}, 'B': {}}
    g = _make_graph(graph)
    with pytest.raises(KeyError) as exc:
        g.depth_traversal('X')
    assert 'X not in graph.' in str(exc.value)

# Teste com ciclo: evita recursão infinita entre A e B e preserva a ordem
def test_depth_traversal_cycle_prevents_infinite_and_order():
    graph = {'A': {'B': {}, 'C': {}}, 'B': {'A': {}}, 'C': {}}
    g = _make_graph(graph)
    assert g.depth_traversal('A') == ['A', 'B', 'C']
