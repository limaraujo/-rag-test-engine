from repositorios.code_katas.src.flight_graph import Graph

# curto: happy path - encontra caminho A->B->D com peso 9
def test_dijkstra_happy_path():
    g = Graph()
    g.graph = {
        'A': {'B': 5},
        'B': {'D': 4},
        'C': {},
        'D': {}
    }
    assert g.dijkstra('A', 'D') == {9: ['A', 'B', 'D']}

# curto: caminho não existente - retorna None
def test_dijkstra_no_path_returns_none():
    g = Graph()
    g.graph = {
        'A': {'B': 1},
        'B': {},
        'C': {}
    }
    assert g.dijkstra('A', 'C') is None

# curto: start é finish - retorna caminho trivial
def test_dijkstra_start_equals_finish():
    g = Graph()
    g.graph = {
        'A': {'B': 2},
        'B': {}
    }
    assert g.dijkstra('A', 'A') == {0: ['A']}

# curto: escolhe rota mais curta entre duas alternativas
def test_dijkstra_prefers_shortest_path_among_multiple_paths():
    g = Graph()
    g.graph = {
        'A': {'B': 2, 'C': 1},
        'B': {'D': 2},
        'C': {'D': 4},
        'D': {}
    }
    # Caminho mais curto: A->B->D com peso 4
    assert g.dijkstra('A', 'D') == {4: ['A', 'B', 'D']}
