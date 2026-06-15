from repositorios.code_katas.src.flight_graph import Graph

# happy path: shortest path A -> D is A -> C -> D
def test_happy_path_shortest_path_A_to_D():
    graph = {
        'A': {'B': 1, 'C': 4},
        'B': {'D': 5},
        'C': {'D': 1},
        'D': {}
    }
    class FakeSelf:
        def __init__(self, g):
            self.graph = g
        def nodes(self):
            return set(self.graph.keys())
    fake = FakeSelf(graph)
    result = Graph.dijkstra(fake, 'A', 'D')
    assert result == {5: ['A', 'C', 'D']}

# edge: finish is unreachable -> returns None (breaks when min_node is None)
def test_no_path_to_finish_returns_none_when_finish_unreachable():
    graph = {
        'A': {'B': 1},
        'B': {}
    }
    class FakeSelf:
        def __init__(self, g):
            self.graph = g
        def nodes(self):
            return set(self.graph.keys())
    fake = FakeSelf(graph)
    assert Graph.dijkstra(fake, 'A', 'C') is None

# edge: start equals finish -> returns zero distance with single-node path
def test_start_equals_finish_returns_zero_distance_and_single_node_path():
    graph = {
        'A': {},
        'B': {}
    }
    class FakeSelf:
        def __init__(self, g):
            self.graph = g
        def nodes(self):
            return set(self.graph.keys())
    fake = FakeSelf(graph)
    assert Graph.dijkstra(fake, 'A', 'A') == {0: ['A']}

# branch: multiple options from start; choose minimum total weight path
def test_min_weight_path_selection_prefers_shortest_between_two_options():
    graph = {
        'A': {'B': 1, 'C': 2},
        'B': {'D': 100},
        'C': {'D': 2},
        'D': {}
    }
    class FakeSelf:
        def __init__(self, g):
            self.graph = g
        def nodes(self):
            return set(self.graph.keys())
    fake = FakeSelf(graph)
    assert Graph.dijkstra(fake, 'A', 'D') == {4: ['A', 'C', 'D']}
