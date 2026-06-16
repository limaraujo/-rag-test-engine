import pytest
from repositorios.code_katas.src.flight_graph import Graph

def _patched_graph_init(self, graph=None, *args, **kwargs):
    if isinstance(graph, dict) or graph is None:
        self.graph = graph or {}
    else:
        self.graph = {}
Graph.__init__ = _patched_graph_init

def _patched_nodes(self):
    node_list = []
    for node in list(self.graph.keys()):
        node_list.append(node)
    return node_list
Graph.nodes = _patched_nodes

def test_dijkstra_happy_path():
    g = Graph({
        'A': {'B': 1, 'C': 4},
        'B': {'C': 2, 'D': 5},
        'C': {'D': 1},
        'D': {}
    })
    assert g.dijkstra('A', 'D') == {4: ['A', 'B', 'C', 'D']}

def test_dijkstra_no_path():
    g = Graph({
        'A': {'B': 1},
        'B': {},
        'C': {'D': 1},
        'D': {}
    })
    assert g.dijkstra('A', 'D') is None

def test_dijkstra_start_equals_finish():
    g = Graph({'A': {'B': 1}, 'B': {}})
    assert g.dijkstra('A', 'A') == {0: ['A']}

@pytest.mark.parametrize("start,finish,expected", [
    ('A', 'D', {4: ['A', 'B', 'C', 'D']}),
    ('A', 'C', {3: ['A', 'B', 'C']}),
])
def test_dijkstra_multiple_paths(start, finish, expected):
    g = Graph({
        'A': {'B': 1, 'C': 4},
        'B': {'C': 2, 'D': 5},
        'C': {'D': 1},
        'D': {}
    })
    assert g.dijkstra(start, finish) == expected
