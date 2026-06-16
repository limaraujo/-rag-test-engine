import pytest
from repositorios.code_katas.src.flight_graph import Graph


# happy path: ensure depth-first traversal returns nodes in pre-order for a simple graph
def test_depth_traversal_happy_path():
    # curto: happy path with deterministic edge order
    g = Graph()
    g.graph = {
        'A': {'B': {}, 'C': {}},
        'B': {'D': {}},
        'C': {'E': {}},
        'D': {},
        'E': {},
    }

    result = g.depth_traversal('A')
    assert result == ['A', 'B', 'D', 'C', 'E']

# edge case: starting node not present in the graph should raise KeyError
def test_depth_traversal_missing_key_raises_keyerror():
    # curto: exception path for missing key
    g = Graph()
    g.graph = {
        'A': {'B': {}},
        'B': {}
    }

    with pytest.raises(KeyError) as excinfo:
        g.depth_traversal('Z')
    assert 'Z not in graph' in str(excinfo.value)

# using an existing checked list to verify it is respected (and not recreated)
def test_depth_traversal_with_existing_checked_list():
    # curto: branch where checked is provided (not None)
    g = Graph()
    g.graph = {
        'A': {'B': {}, 'C': {}},
        'B': {'D': {}},
        'C': {'E': {}},
        'D': {},
        'E': {},
    }

    initial_checked = ['X']
    result = g.depth_traversal('A', initial_checked)
    assert result == ['X', 'A', 'B', 'D', 'C', 'E']
