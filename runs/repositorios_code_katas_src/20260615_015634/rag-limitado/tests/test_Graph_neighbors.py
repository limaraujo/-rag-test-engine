import pytest
from repositorios.code_katas.src.flight_graph import Graph

# happy path: node exists, returns its neighbor list
def test_neighbors_happy_path():
    g = Graph.__new__(Graph)
    g.graph = {'A': ['B', 'C'], 'B': ['A']}
    assert g.neighbors('A') == ['B', 'C']

# edge case: requested node not in graph raises KeyError
def test_neighbors_missing_key_raises_keyerror():
    g = Graph.__new__(Graph)
    g.graph = {'A': ['B']}
    with pytest.raises(KeyError) as excinfo:
        g.neighbors('X')
    assert "Not in graph." in str(excinfo.value)
