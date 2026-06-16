import pytest
from repositorios.code_katas.src.flight_graph import Graph

# Verifica has_node para cenários: nó existente (True) e nó ausente (False)
@pytest.mark.parametrize("node,exists", [
    ("A", True),
    ("C", False),
])
def test_has_node_various_nodes(node, exists):
    g = Graph()
    g.graph = {"A": [], "B": []}
    assert g.has_node(node) is exists
