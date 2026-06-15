import pytest
from repositorios.code_katas.src.flight_graph import Graph

def _make_graph(mapping):
    g = Graph()
    g.graph = mapping
    return g


# Testar caminho feliz: retorna dicionário de vizinhos para nó existente com dois vizinhos
def test_neighbors_happy_path():
    g = _make_graph({'A': {'B': 1, 'C': 2}, 'B': {'A': 1}, 'C': {'A': 2}})
    assert g.neighbors('A') == {'B': 1, 'C': 2}


# Teste de exceção: nó não está presente no grafo
def test_neighbors_missing_key_raises():
    g = _make_graph({'A': {'B': 1}})
    with pytest.raises(KeyError) as exc:
        g.neighbors('D')
    assert exc.value.args[0] == "Not in graph."


# Teste de borda: nó existente, mas sem vizinhos
def test_neighbors_empty_neighbors():
    g = _make_graph({'A': {}, 'B': {'A': 1}})
    assert g.neighbors('A') == {}


# Teste de caso simples: nó existente com único vizinho
def test_neighbors_single_neighbor():
    g = _make_graph({'A': {'B': 5}, 'B': {'A': 5}})
    assert g.neighbors('A') == {'B': 5}
