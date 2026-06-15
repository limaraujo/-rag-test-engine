import pytest
from repositorios.code_katas.src.flight_graph import Graph

def _build_graph(graph):
    g = Graph()
    g.graph = graph
    return g

def test_breadth_traversal_happy_path():
    graph = {
        'A': {'B': {}, 'C': {}},
        'B': {'D': {}},
        'C': {'D': {}},
        'D': {}
    }
    g = _build_graph(graph)
    assert g.breadth_traversal('A') == ['A', 'B', 'C', 'D']

def test_breadth_traversal_start_missing_raises_keyerror():
    graph = {'A': {'B': {}}}
    g = _build_graph(graph)
    with pytest.raises(KeyError):
        g.breadth_traversal('X')

def test_breadth_traversal_handles_duplicate_in_queue():
    graph = {
        'A': {'B': {}, 'C': {}},
        'B': {'D': {}},
        'C': {'D': {}},
        'D': {}
    }
    g = _build_graph(graph)
    assert g.breadth_traversal('A') == ['A', 'B', 'C', 'D']
