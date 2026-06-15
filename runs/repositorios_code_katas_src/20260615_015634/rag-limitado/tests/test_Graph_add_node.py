import pytest
from repositorios.code_katas.src.flight_graph import Graph

# Verifica adicionando um nó que não existe (caminho feliz)
def test_add_node_happy_path():
    g = Graph()
    g.add_node("A")
    assert g.graph == {"A": {}}

# Verifica raising de KeyError ao tentar adicionar um nó já existente (exceção)
def test_add_node_duplicate_raises_keyerror():
    g = Graph()
    g.graph["A"] = {}
    with pytest.raises(KeyError):
        g.add_node("A")
