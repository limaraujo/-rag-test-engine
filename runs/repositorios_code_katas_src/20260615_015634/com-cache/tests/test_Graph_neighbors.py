import pytest
from repositorios.code_katas.src.flight_graph import Graph

# curto: caminho feliz - retorna dicionário de vizinhos para um nó existente
def test_neighbors_happy_path():
    g = Graph()
    g.graph = {
        'A': {'B': 1, 'C': 2},
        'B': {'A': 1},
        'C': {'A': 2}
    }
    assert g.neighbors('A') == {'B': 1, 'C': 2}

# curto: exceção KeyError - nó ausente levanta KeyError
def test_neighbors_missing_key():
    g = Graph()
    g.graph = {'A': {'B': 1}}
    with pytest.raises(KeyError):
        g.neighbors('Z')

# curto: caminho feliz - nó existente com nenhum vizinho retorna dicionário vazio
def test_neighbors_empty_neighbors():
    g = Graph()
    g.graph = {'A': {}, 'B': {'A': 1}}
    assert g.neighbors('A') == {}
