import pytest
from repositorios.code_katas.src.flight_graph import Graph

# Verifica o caminho feliz: apaga edge existente quando node2 tem adjacências
def test_del_edge_happy_path():
    # happy path: edge A->B exists and B has outgoing edges
    g = Graph()
    g.graph = {
        'A': {'B': 1, 'C': 2},
        'B': {'C': 3},
        'C': {}
    }

    g.del_edge('A', 'B')

    assert 'B' not in g.graph['A']
    assert g.graph['A']['C'] == 2
    assert g.graph['B']['C'] == 3

# Verifica comportamento para chave ausente no vértice de origem (KeyError)
def test_del_edge_missing_source_node_raises_KeyError():
    # invalid_input: source node não existe
    g = Graph()
    g.graph = {
        'A': {'B': 1},
        'B': {'C': 2}
    }

    with pytest.raises(KeyError):
        g.del_edge('X', 'A')

# Verifica ValueError quando edge não existe, mas ambos nodes existem
def test_del_edge_edge_not_present_raises_ValueError():
    # edge não existente entre A e B -> ValueError
    g = Graph()
    g.graph = {
        'A': {'C': 1},
        'B': {'C': 2},
        'C': {}
    }

    with pytest.raises(ValueError):
        g.del_edge('A', 'B')

# Verifica ValueError quando edge existe, mas node2 não possui outgoing edges
def test_del_edge_edge_exists_but_node2_has_no_outgoing_raises_ValueError():
    # edge A->B existe, porém B não tem adjacências -> ValueError
    g = Graph()
    g.graph = {
        'A': {'B': 1},
        'B': {},  # node2 sem adjacências
        'C': {}
    }

    with pytest.raises(ValueError):
        g.del_edge('A', 'B')
