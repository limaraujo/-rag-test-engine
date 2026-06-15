import pytest
from repositorios.code_katas.src.flight_graph import Graph

# Verifica o comportamento básico com chaves de string (casos de sucesso e falha)
@pytest.mark.parametrize("graph_dict, node, expected", [
    ({"A": [], "B": []}, "A", True),
    ({"A": [], "B": []}, "C", False),
])
def test_has_node_string_keys(graph_dict, node, expected):
    g = Graph()
    g.graph = graph_dict
    assert g.has_node(node) == expected

# Verifica o comportamento com chaves numéricas (tipos diferentes, casos de borda)
def test_has_node_numeric_keys():
    g = Graph()
    g.graph = {1: [], 2: []}
    assert g.has_node(1) == True
    assert g.has_node(3) == False
