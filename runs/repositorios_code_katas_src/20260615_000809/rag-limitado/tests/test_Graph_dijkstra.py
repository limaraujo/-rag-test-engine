from repositorios.code_katas.src.flight_graph import Graph

def test_dijkstra_happy_path_shortest():
    graph = {
        'A': {'B': 5, 'C': 1},
        'B': {'D': 2},
        'C': {'D': 4},
        'D': {}
    }
    g = Graph()
    g.graph = graph
    assert g.dijkstra('A', 'D') == {5: ['A', 'C', 'D']}

def test_dijkstra_equal_paths_tie_breaker():
    graph = {
        'A': {'B': 2, 'C': 3},
        'B': {'D': 3},
        'C': {'D': 2},
        'D': {}
    }
    g = Graph()
    g.graph = graph
    assert g.dijkstra('A', 'D') == {5: ['A', 'B', 'D']}

def test_dijkstra_no_path_returns_none():
    graph = {
        'A': {'B': 1},
        'B': {'A': 1},
        'C': {'D': 1},
        'D': {'C': 1}
    }
    g = Graph()
    g.graph = graph
    assert g.dijkstra('A', 'D') is None

def test_dijkstra_start_equals_finish_returns_zero_path():
    graph = {
        'A': {'B': 5},
        'B': {'A': 5}
    }
    g = Graph()
    g.graph = graph
    assert g.dijkstra('A', 'A') == {0: ['A']}
