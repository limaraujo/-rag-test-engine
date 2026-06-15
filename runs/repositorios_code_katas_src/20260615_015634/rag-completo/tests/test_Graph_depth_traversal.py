import pytest
from repositorios.code_katas.src.flight_graph import Graph

# testa caminho principal (happy path): A -> B -> C a partir de A
def test_depth_traversal_happy_path_chain():
    g = Graph()
    g.graph = {'A': {'B': None}, 'B': {'C': None}, 'C': {}}
    assert g.depth_traversal('A') == ['A', 'B', 'C']

# testa ciclo simples para confirmar que evita recursão infinita
def test_depth_traversal_cycle():
    g = Graph()
    g.graph = {'A': {'B': None}, 'B': {'A': None}}
    assert g.depth_traversal('A') == ['A', 'B']

# testando KeyError quando o nó inicial não existe no grafo
def test_depth_traversal_missing_start_key_raises():
    g = Graph()
    g.graph = {'A': {'B': None}}
    with pytest.raises(KeyError) as excinfo:
        g.depth_traversal('Z')
    assert 'Z not in graph.' in str(excinfo.value)

# testando KeyError quando há dependência para nó ausente (caminho quebrado)
def test_depth_traversal_missing_child_raises():
    g = Graph()
    g.graph = {'A': {'B': None}}
    with pytest.raises(KeyError) as excinfo:
        g.depth_traversal('A')
    assert 'B not in graph.' in str(excinfo.value)
