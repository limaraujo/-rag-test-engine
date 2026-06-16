import pytest
from repositorios.code_katas.src.flight_graph import Graph

# Verifica Graph.nodes retorna os nós na ordem de inserção (vazio, único, múltiplos)
@pytest.mark.parametrize("insert_sequence, expected", [
    ([], []),
    (['A'], ['A']),
    (['A', 'B', 'C'], ['A', 'B', 'C']),
])
def test_nodes_returns_insertion_order(insert_sequence, expected):
    g = Graph()
    for node in insert_sequence:
        g.add_node(node)
    assert g.nodes() == expected
