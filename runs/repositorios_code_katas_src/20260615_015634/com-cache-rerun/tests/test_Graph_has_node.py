import pytest
from repositorios.code_katas.src.flight_graph import Graph

# curto: caminho feliz - has_node após adicionar aresta entre A e B: A e B presentes, C/None ausentes
@pytest.mark.parametrize("node,expected", [
    ("A", True),
    ("B", True),
    ("C", False),
    (None, False),
])
def test_has_node_after_adding_edge(node, expected):
    g = Graph()
    g.add_edge("A", "B")
    assert g.has_node(node) == expected
