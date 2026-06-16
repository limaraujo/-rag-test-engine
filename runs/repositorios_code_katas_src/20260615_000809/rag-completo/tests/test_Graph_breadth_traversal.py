import pytest
from repositorios.code_katas.src.flight_graph import Graph

# Test: happy path - BFS visits nodes in expected order for a simple connected graph
def test_breadth_traversal_happy_path_basic():
    graph = {
        'A': {'B': {}, 'C': {}},
        'B': {'A': {}, 'D': {}},
        'C': {'A': {}},
        'D': {'B': {}}
    }
    g = Graph()
    g.graph = graph
    assert g.breadth_traversal('A') == ['A', 'B', 'C', 'D']

# Test: starting node not present in graph raises KeyError (indirectly via dict lookup)
def test_breadth_traversal_start_not_in_graph_raises():
    graph = {
        'A': {'B': {}},
        'B': {'A': {}}
    }
    g = Graph()
    g.graph = graph
    with pytest.raises(KeyError):
        g.breadth_traversal('X')

# Test: traversal limited to connected component (disconnected graph)
def test_breadth_traversal_disconnected_component():
    graph = {
        'A': {'B': {}, 'C': {}},
        'B': {'A': {}},
        'C': {'A': {}},
        'D': {'E': {}},
        'E': {'D': {}}
    }
    g = Graph()
    g.graph = graph
    assert g.breadth_traversal('A') == ['A', 'B', 'C']

GRAPH_ORDER_VARIANTS = [
    (
        {
            'A': {'B': {}, 'C': {}},
            'B': {'A': {}, 'D': {}},
            'C': {'A': {}},
            'D': {'B': {}}
        },
        'A',
        ['A', 'B', 'C', 'D']
    ),
    (
        {
            'A': {'C': {}, 'B': {}},
            'B': {'A': {}, 'D': {}},
            'C': {'A': {}},
            'D': {'B': {}}
        },
        'A',
        ['A', 'C', 'B', 'D']
    ),
]

# Test: order of BFS respects insertion order of edges (branch coverage)
@pytest.mark.parametrize("graph,start,expected", GRAPH_ORDER_VARIANTS)
def test_breadth_traversal_order_variants(graph, start, expected):
    g = Graph()
    g.graph = graph
    assert g.breadth_traversal(start) == expected
