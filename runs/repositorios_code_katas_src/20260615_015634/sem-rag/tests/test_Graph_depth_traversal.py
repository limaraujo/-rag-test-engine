import pytest
from repositorios.code_katas.src.flight_graph import Graph

# happy path: traversal from A visits B, D, C, E in DFS order
def test_depth_traversal_happy_path():
    g = Graph()
    g.graph = {
        'A': {'B': None, 'C': None},
        'B': {'D': None},
        'D': {},
        'C': {'E': None},
        'E': {}
    }
    result = g.depth_traversal('A')
    assert result == ['A', 'B', 'D', 'C', 'E']

# branch: cycle between A and B should not cause infinite recursion
def test_depth_traversal_cycle():
    g = Graph()
    g.graph = {
        'A': {'B': None},
        'B': {'A': None}
    }
    result = g.depth_traversal('A')
    assert result == ['A', 'B']

# branch: non-None checked parameter is used to accumulate results
def test_depth_traversal_with_preexisting_checked():
    g = Graph()
    g.graph = {
        'A': {'B': None, 'C': None},
        'B': {'D': None},
        'D': {},
        'C': {'E': None},
        'E': {}
    }
    result = g.depth_traversal('A', checked=['PRE'])
    assert result == ['PRE', 'A', 'B', 'D', 'C', 'E']

# exception path: start key not in graph raises KeyError with expected message
def test_depth_traversal_missing_key_raises():
    g = Graph()
    g.graph = {
        'A': {'B': None},
        'B': {}
    }
    with pytest.raises(KeyError) as exc:
        g.depth_traversal('Z')
    assert exc.value.args[0] == 'Z not in graph.'
