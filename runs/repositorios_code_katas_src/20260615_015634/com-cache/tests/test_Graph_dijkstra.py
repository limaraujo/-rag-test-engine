from repositorios.code_katas.src.flight_graph import Graph

# curto: happy path - dijkstra encontra caminho A->B->D com peso 9
def test_dijkstra_happy_path():
    g = Graph()
    g.graph = {
        'A': {'B': 5},
        'B': {'D': 4},
        'C': {},
        'D': {}
    }
    assert g.dijkstra('A', 'D') == {9: ['A', 'B', 'D']}

# curto: caminho impossível - finish não alcançável retorna None
def test_dijkstra_unreachable_finish():
    g = Graph()
    g.graph = {
        'A': {'B': 2},
        'B': {},
        'C': {}
    }
    assert g.dijkstra('A', 'D') is None

# curto: path vs alternative - escolhe caminho mais curto entre A->D (A-B-D vs A-C-D)
def test_dijkstra_shortest_among_two_paths():
    g = Graph()
    g.graph = {
        'A': {'B': 1, 'C': 2},
        'B': {'D': 4},
        'C': {'D': 2},
        'D': {}
    }
    assert g.dijkstra('A', 'D') == {4: ['A', 'C', 'D']}

# curto: caso borda - start == finish retorna caminho trivial [start]
def test_dijkstra_start_equals_finish():
    g = Graph()
    g.graph = {
        'A': {'B': 3},
        'B': {}
    }
    assert g.dijkstra('A', 'A') == {0: ['A']}
