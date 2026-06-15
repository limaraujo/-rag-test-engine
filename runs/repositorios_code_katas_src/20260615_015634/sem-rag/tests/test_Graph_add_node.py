import pytest
from repositorios.code_katas.src.flight_graph import Graph

# Teste happy path: adiciona nó novo em grafo vazio
def test_add_node_happy_path():
    g = Graph()
    g.graph = {}
    g.add_node("A")
    assert "A" in g.graph
    assert g.graph["A"] == {}

# Teste tenta adicionar nó existente: espera KeyError
def test_add_node_existing_node_raises_keyerror():
    g = Graph()
    g.graph = {"A": {}}
    with pytest.raises(KeyError) as exc:
        g.add_node("A")
    assert "Node already in graph." in str(exc.value)

# Teste nó não-hashável causa TypeError ao inserir
def test_add_node_unhashable_node_raises_typeerror():
    g = Graph()
    g.graph = {}
    with pytest.raises(TypeError):
        g.add_node([])

# Teste edge case missing_key: atributo graph ausente gera AttributeError
def test_add_node_missing_graph_attribute_raises_attribute_error():
    g = Graph.__new__(Graph)  # não chama __init__, graph não é inicializado
    with pytest.raises(AttributeError):
        g.add_node("A")
