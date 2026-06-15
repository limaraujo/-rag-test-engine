from repositorios.code_katas.src.flight_graph import Graph

# Test 1: happy path - simple A -> B -> C with total distance 2
def test_dijkstra_happy_path_simple():
    g = Graph()
    g.graph = {
        'A': {'B': 1, 'C': 4},
        'B': {'C': 1},
        'C': {}
    }
    assert g.dijkstra('A', 'C') == {2: ['A', 'B', 'C']}

# Test 2: no path exists between start and finish
def test_dijkstra_no_path():
    g = Graph()
    g.graph = {
        'A': {'B': 1},
        'B': {},
        'D': {}
    }
    assert g.dijkstra('A', 'D') is None

# Test 3: choose shorter path when multiple routes exist
def test_dijkstra_prefers_shorter_path():
    g = Graph()
    g.graph = {
        'A': {'B': 2, 'C': 1},
        'B': {'D': 2},
        'C': {'D': 5},
        'D': {}
    }
    assert g.dijkstra('A', 'D') == {4: ['A', 'B', 'D']}

# Test 4: start and finish are the same node
def test_dijkstra_start_equals_finish():
    g = Graph()
    g.graph = {
        'X': {}
    }
    assert g.dijkstra('X', 'X') == {0: ['X']}
