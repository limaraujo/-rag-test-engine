import pytest
from repositorios.code_katas.src.flight_graph import Graph

# happy path: existing node returns its neighbors
def test_neighbors_happy_path():
    g = Graph()
    g.graph = {'A': ['B', 'C'], 'B': ['A'], 'C': ['A']}
    assert g.neighbors('A') == ['B', 'C']

# exception KeyError: node not in graph
def test_neighbors_missing_key_raises_keyerror():
    g = Graph()
    g.graph = {'X': ['Y']}
    with pytest.raises(KeyError) as exc:
        g.neighbors('Z')
    assert exc.value.args[0] == "Not in graph."
