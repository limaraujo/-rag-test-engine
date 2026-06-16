from repositorios.code_katas.src.flight_graph import Graph

# teste feliz: BFS simples com A -> B, C; D é filho de B
def test_breadth_traversal_basic_happy_path():
    g = Graph()
    g.graph = {
        'A': {'B': 1, 'C': 1},
        'B': {'D': 1},
        'C': {},
        'D': {}
    }
    assert g.breadth_traversal('A') == ['A', 'B', 'C', 'D']

# teste com ramificações múltiplas: A leva a B e C; B leva a E; C leva a F
def test_breadth_traversal_multiple_branches():
    g = Graph()
    g.graph = {
        'A': {'B': 1, 'C': 1},
        'B': {'E': 1},
        'C': {'F': 1},
        'E': {},
        'F': {}
    }
    assert g.breadth_traversal('A') == ['A', 'B', 'C', 'E', 'F']

# teste com ciclo: garante que BFS não entra em loop com A<->B
def test_breadth_traversal_handles_cycle():
    g = Graph()
    g.graph = {
        'A': {'B': 1},
        'B': {'A': 1}
    }
    assert g.breadth_traversal('A') == ['A', 'B']
