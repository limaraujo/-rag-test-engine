import pytest
from repositorios.code_katas.src.flight_graph import Graph

# Verifica edges em cenários: grafo não vazio (caminho principal) e grafo vazio (caso de borda)
@pytest.mark.parametrize("graph, expected", [
    (
        {"A": {"B": 1, "C": 2}, "B": {"C": 3}, "C": {}},
        ["A: ['B', 'C']", "B: ['C']", "C: []"]
    ),
    ({}, [])
])
def test_edges(graph, expected):
    g = Graph()
    g.graph = graph
    assert g.edges() == expected
