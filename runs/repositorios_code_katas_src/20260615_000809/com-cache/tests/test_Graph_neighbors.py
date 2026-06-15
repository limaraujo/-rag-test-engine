import pytest
from repositorios.code_katas.src.flight_graph import Graph

# teste: caminho feliz - um único edge: neighbors retorna o dicionário de vizinhos incluindo o destino
def test_neighbors_happy_path_single_edge():
    g = Graph()
    g.add_edge("A", "B")
    assert "B" in g.neighbors("A")
    assert "A" not in g.neighbors("A")

# teste: caminho com múltiplos edges a partir do mesmo nó: neighbors retorna todos os vizinhos
def test_neighbors_multiple_edges():
    g = Graph()
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    neigh = g.neighbors("A")
    assert isinstance(neigh, dict)
    assert set(neigh.keys()) == {"B", "C"}

# teste: caso de borda - chave ausente levanta KeyError
def test_neighbors_missing_key_raises():
    g = Graph()
    with pytest.raises(KeyError) as excinfo:
        g.neighbors("X")
    assert "Not in graph." in str(excinfo.value)
