import pytest
from repositorios.code_katas.src.flight_graph import Graph

# curto: has_node - verifica retorno True para nós existentes (A,B) e False para ausentes (C, None)
@pytest.mark.parametrize("node,expected", [
    ("A", True),
    ("B", True),
    ("C", False),
    (None, False),
])
def test_has_node_parametric(node, expected):
    g = Graph()
    g.add_node("A")
    g.add_node("B")
    assert g.has_node(node) is expected
