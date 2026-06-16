import pytest
from repositorios.code_katas.src.flight_graph import Graph

def _make_graph(graph_dict):
    g = Graph.__new__(Graph)
    g.graph = graph_dict
    return g

# short: happy path - BFS from A should visit A, then B and C, then D
def test_breadth_traversal_happy_path():
    graph = {
        'A': {'B': {}, 'C': {}},
        'B': {'D': {}},
        'C': {'D': {}},
        'D': {}
    }
    g = _make_graph(graph)
    assert g.breadth_traversal('A') == ['A', 'B', 'C', 'D']

# short: branch coverage - graph produces a duplicate in the queue to exercise the else branch
def test_breadth_traversal_handles_duplicate_in_queue():
    graph = {
        'A': {'B': {}, 'C': {}},
        'B': {'C': {}},
        'C': {'B': {}}
    }
    g = _make_graph(graph)
    # Expected traversal order remains deterministic for the given structure
    assert g.breadth_traversal('A') == ['A', 'B', 'C']

# short: excepcão listada - começar em nó que não existe lança KeyError
def test_breadth_traversal_start_missing_key_raises():
    graph = {'X': {}}
    g = _make_graph(graph)
    with pytest.raises(KeyError):
        g.breadth_traversal('Y')
