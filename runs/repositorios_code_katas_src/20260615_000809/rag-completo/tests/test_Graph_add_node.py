import pytest
from repositorios.code_katas.src.flight_graph import Graph

# curto: happy path - adiciona novo nó ausente no grafo vazio
def test_add_node_happy_path():
    g = Graph()
    g.add_node("A")
    assert g.nodes() == ["A"]
    assert g.graph["A"] == {}

# curto: exceção KeyError ao adicionar nó já existente
def test_add_node_duplicate_raises():
    g = Graph()
    g.add_node("A")
    with pytest.raises(KeyError):
        g.add_node("A")

# curto: múltiplos nós - verifica ordem e estrutura do grafo
def test_add_node_multiple_nodes():
    g = Graph()
    g.add_node("A")
    g.add_node("B")
    assert g.nodes() == ["A", "B"]
    assert g.graph["A"] == {}
    assert g.graph["B"] == {}

# curto: borda com chave não string - comportamento genérico
def test_add_node_non_string_key():
    g = Graph()
    g.add_node(1)
    assert g.nodes() == [1]
    assert g.graph[1] == {}
