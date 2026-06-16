import pytest
from repositorios.code_katas.src.flight_graph import Graph

# Verifica edges() para grafos com várias arestas (happy path) e nó sem arestas (caso de borda)
@pytest.mark.parametrize("graph_dict, expected", [
    (
        {'A': {'B': 1, 'C': 2}, 'B': {'C': 3}, 'C': {}},
        ["A: ['B', 'C']", "B: ['C']", "C: []"]
    ),
    (
        {'D': {}, 'E': {'F': 7}},
        ["D: []", "E: ['F']"]
    ),
])
def test_edges_returns_expected_strings(graph_dict, expected):
    g = Graph()
    g.graph = graph_dict
    assert g.edges() == expected
