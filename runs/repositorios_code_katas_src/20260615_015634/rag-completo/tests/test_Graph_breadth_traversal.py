import pytest
from repositorios.code_katas.src.flight_graph import Graph


# Helper to create a Graph-like instance without invoking __init__
def _make_graph(graph_dict):
    g = Graph.__new__(Graph)
    g.graph = graph_dict
    return g

# Test 1: happy path - verifica a traversão em largura em gráfico simples sem ciclos
def test_breadth_traversal_happy_path():
    g = _make_graph({
        'A': {'B': 1, 'C': 1},
        'B': {'D': 1},
        'C': {'D': 1},
        'D': {}
    })
    assert g.breadth_traversal('A') == ['A', 'B', 'C', 'D']

# Test 2: cycle handling - assegura que não haja duplicação de nós em ciclos
def test_breadth_traversal_cycle_no_duplicates():
    g = _make_graph({
        'A': {'B': 1, 'C': 1},
        'B': {'A': 1},
        'C': {'A': 1}
    })
    assert g.breadth_traversal('A') == ['A', 'B', 'C']

# Test 3: erro ao iniciar a partir de nó ausente - KeyError esperado
def test_breadth_traversal_missing_start_raises_keyerror():
    g = _make_graph({'A': {'B': 1}})
    with pytest.raises(KeyError):
        g.breadth_traversal('X')
