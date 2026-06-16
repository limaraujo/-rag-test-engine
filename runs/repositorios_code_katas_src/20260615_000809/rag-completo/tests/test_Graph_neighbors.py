import pytest
from repositorios.code_katas.src.flight_graph import Graph

# caminho feliz: verifica que neighbors retorna os vizinhos de um nó existente
def test_neighbors_happy_path():
    g = Graph()
    g.graph = {
        'A': {'B': 1, 'C': 2},
        'B': {'A': 1},
        'C': {'A': 2}
    }
    assert g.neighbors('A') == {'B': 1, 'C': 2}

# exceção: verifica que uma chave ausente levanta KeyError com a mensagem esperada
def test_neighbors_missing_key_raises_KeyError():
    g = Graph()
    g.graph = {
        'X': {'Y': 1}
    }
    with pytest.raises(KeyError, match="Not in graph."):
        g.neighbors('Z')

# caso de borda: nó existente com lista de vizinhos vazia
def test_neighbors_empty_connections():
    g = Graph()
    g.graph = {
        'D': {}
    }
    assert g.neighbors('D') == {}
