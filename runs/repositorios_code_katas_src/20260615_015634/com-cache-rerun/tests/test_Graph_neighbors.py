import pytest
from repositorios.code_katas.src.flight_graph import Graph

# curto: caminho feliz - nó existente com vizinhos não vazios
def test_neighbors_happy_path():
    g = Graph()
    g.graph = {
        'A': {'B': 1, 'C': 2},
        'B': {'A': 1},
        'C': {'A': 2}
    }
    assert g.neighbors('A') == {'B': 1, 'C': 2}

# curto: exceção - chave ausente levanta KeyError
def test_neighbors_missing_key_raises():
    g = Graph()
    g.graph = {'A': {'B': 1}}
    with pytest.raises(KeyError) as excinfo:
        g.neighbors('B')
    assert excinfo.value.args[0] == "Not in graph."

# curto: caminho feliz - nó existente mas sem vizinhos retorna dict vazio
def test_neighbors_empty_neighbors():
    g = Graph()
    g.graph = {'A': {}}
    assert g.neighbors('A') == {}
