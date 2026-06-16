import pytest
from repositorios.code_katas.src.flight_graph import Graph

# short: happy path - verify neighbors returns the list for an existing node
def test_neighbors_happy_path():
    g = Graph()
    g.graph = {"A": ["B", "C"], "B": ["A"]}
    assert g.neighbors("A") == ["B", "C"]

# short: missing key - verify KeyError is raised for a node not in the graph
def test_neighbors_missing_key_raises_keyerror():
    g = Graph()
    g.graph = {"A": ["B"]}
    with pytest.raises(KeyError) as excinfo:
        g.neighbors("Z")
    assert str(excinfo.value) == "'Not in graph.'"
