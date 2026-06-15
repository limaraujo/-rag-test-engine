import pytest
from repositorios.code_katas.src.flight_graph import Graph

# Verifica caminho principal: DFS simples sem ciclos e visita todos os nós alcançáveis (happy path)
def test_depth_traversal_happy_path_basic():
    g = Graph()
    g.graph = {
        'A': {'B': None, 'C': None},
        'B': {'D': None},
        'C': {},
        'D': {}
    }
    result = g.depth_traversal('A')
    assert set(result) == {'A', 'B', 'C', 'D'}

# Verifica manejo de ciclos: evita recursão infinita e retorna apenas nós únicos visitados
def test_depth_traversal_cycle_handling():
    g = Graph()
    g.graph = {
        'A': {'B': None},
        'B': {'A': None}
    }
    result = g.depth_traversal('A')
    assert set(result) == {'A', 'B'}

# Verifica exceção KeyError ao iniciar em chave ausente do grafo
def test_depth_traversal_missing_start_raises_keyerror():
    g = Graph()
    g.graph = {'X': {}}
    with pytest.raises(KeyError) as exc:
        g.depth_traversal('Y')
    assert 'Y not in graph.' in str(exc.value)

# Verifica exceção KeyError ao encontrar nó intermediário ausente durante a travessia
def test_depth_traversal_missing_intermediate_raises_keyerror():
    g = Graph()
    g.graph = {'A': {'B': None}, 'B': {'C': None}}  # C ausente
    with pytest.raises(KeyError) as exc:
        g.depth_traversal('A')
    assert 'C not in graph.' in str(exc.value)
