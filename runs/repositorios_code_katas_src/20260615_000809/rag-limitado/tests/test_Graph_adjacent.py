import pytest
from repositorios.code_katas.src.flight_graph import Graph

# Teste: caminho feliz (happy path) - edge existente entre A e B (em pelo menos uma direção)
def test_adjacent_happy_path_true_bidirectional():
    g = Graph()
    g.graph = {
        "A": {"B": {}},
        "B": {"A": {}}
    }
    assert g.adjacent("A", "B") is True

# Teste: exceção KeyError quando o primeiro nó não existe no grafo
def test_adjacent_missing_node1_raises():
    g = Graph()
    g.graph = {
        "A": {"B": {}},
        "B": {"A": {}}
    }
    with pytest.raises(KeyError):
        g.adjacent("X", "A")

# Teste: exceção KeyError quando o segundo nó não existe no grafo (e o primeiro existe)
def test_adjacent_missing_node2_raises():
    g = Graph()
    g.graph = {
        "A": {"B": {}},
        "B": {"A": {}}
    }
    with pytest.raises(KeyError):
        g.adjacent("A", "X")

# Teste: caso em que os nós existem mas não há aresta entre eles (retorna False)
def test_adjacent_not_connected_returns_false():
    g = Graph()
    g.graph = {
        "A": {"C": {}},
        "B": {"D": {}}
    }
    assert g.adjacent("A", "B") is False
