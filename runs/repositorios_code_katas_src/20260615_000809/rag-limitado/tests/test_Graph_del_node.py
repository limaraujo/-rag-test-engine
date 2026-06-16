import pytest
from repositorios.code_katas.src.flight_graph import Graph

# Testa deleção de nó existente (happy path) removendo o nó e limpando referências
def test_del_node_happy_path():
    g = Graph()
    g.graph = {
        'A': {'B': 1, 'C': 2},
        'B': {'A': 1},
        'C': {'A': 2}
    }
    g.del_node('A')
    assert 'A' not in g.graph
    assert g.graph == {'B': {}, 'C': {}}

# Testa exceção KeyError ao tentar deletar nó que não existe (missing_key)
def test_del_node_missing_key_raises():
    g = Graph()
    g.graph = {'X': {}}
    with pytest.raises(KeyError):
        g.del_node('Y')

# Testa remoção de referências apenas em alguns vizinhos (um vizinho referencia o nó, outro não)
def test_del_node_partial_reference_removal():
    g = Graph()
    g.graph = {
        'A': {'B': 1, 'C': 2},
        'B': {},        # não referencia A
        'C': {'A': 2}    # referencia A
    }
    g.del_node('A')
    assert 'A' not in g.graph
    assert g.graph == {
        'B': {},
        'C': {}
    }
