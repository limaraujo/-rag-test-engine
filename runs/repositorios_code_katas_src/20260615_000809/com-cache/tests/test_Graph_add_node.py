import pytest
from repositorios.code_katas.src.flight_graph import Graph


# Teste feliz: adiciona nó novo ao grafo (caminho feliz)
def test_add_node_happy_path():
    g = Graph()
    g.add_node("A")
    assert "A" in g.graph
    assert g.graph["A"] == {}

# Teste de exceção: tentar adicionar nó já existente levanta KeyError
def test_add_node_duplicate_raises_keyerror():
    g = Graph()
    g.add_node("A")
    with pytest.raises(KeyError):
        g.add_node("A")
