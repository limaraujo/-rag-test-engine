import pytest
from repositorios.code_katas.src.flight_graph import Graph

# Verifica caminho feliz: adiciona novo nó em grafo vazio
def test_add_node_happy_path():
    g = Graph()
    g.add_node("A")
    assert "A" in g.graph
    assert g.graph["A"] == {}

# Verifica exceção quando adicionar nó já existente (branch existente)
def test_add_node_duplicate_raises_keyerror():
    g = Graph()
    g.add_node("A")
    with pytest.raises(KeyError) as exc:
        g.add_node("A")
    assert "Node already in graph." in str(exc.value)
