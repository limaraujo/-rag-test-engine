import pytest
from repositorios.code_katas.src.flight_graph import Graph

# happy path: verifica lista de nós visitados na travessia em largura (ordem determinística)
def test_breadth_traversal_happy_path():
    g = Graph()
    g.graph = {
        'A': {'B': {}, 'C': {}},
        'B': {'D': {}},
        'C': {'D': {}},
        'D': {}
    }
    assert g.breadth_traversal('A') == ['A', 'B', 'C', 'D']

# branch: verifica comportamento com ciclo simples para não reprocessar nós
def test_breadth_traversal_cycle_does_not_revisit():
    g = Graph()
    g.graph = {
        'A': {'B': {}, 'C': {}},
        'B': {'A': {}},
        'C': {}
    }
    assert g.breadth_traversal('A') == ['A', 'B', 'C']

# exception: início não existente levanta KeyError
def test_breadth_traversal_invalid_start_raises_keyerror():
    g = Graph()
    g.graph = {
        'A': {'B': {}},
        'B': {}
    }
    with pytest.raises(KeyError):
        g.breadth_traversal('X')

# edge ordering: verifica ordem de expansão em múltiplasramificações
def test_breadth_traversal_multiple_branches_ordering():
    g = Graph()
    g.graph = {
        'A': {'B': {}, 'C': {}},
        'B': {'D': {}},
        'C': {'E': {}},
        'D': {},
        'E': {}
    }
    assert g.breadth_traversal('A') == ['A', 'B', 'C', 'D', 'E']
