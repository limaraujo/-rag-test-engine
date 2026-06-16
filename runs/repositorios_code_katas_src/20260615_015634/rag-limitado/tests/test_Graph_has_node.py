import pytest
from repositorios.code_katas.src.flight_graph import Graph

# Verifica has_node retorna True para nó existente e False para nó ausente (caso feliz + borda)
@pytest.mark.parametrize("graph_state, node, expected", [
    ({'A': None, 'B': None}, 'A', True),
    ({'A': None, 'B': None}, 'C', False),
])
def test_has_node_exists_and_missing(graph_state, node, expected):
    g = Graph()
    g.graph = graph_state
    assert g.has_node(node) is expected
