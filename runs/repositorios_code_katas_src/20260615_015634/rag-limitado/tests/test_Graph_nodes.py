from repositorios.code_katas.src.flight_graph import Graph

# Happy path: returns all keys in insertion order from a non-empty graph
def test_nodes_happy_path():
    g = Graph.__new__(Graph)
    g.graph = {'A': {}, 'B': {}, 'C': {}}
    result = g.nodes()
    expected = list(g.graph.keys())
    assert result == expected

# Empty graph: returns an empty list
def test_nodes_empty_graph():
    g = Graph.__new__(Graph)
    g.graph = {}
    result = g.nodes()
    assert result == []

# Order preservation: preserves insertion order of keys
def test_nodes_preserves_key_order():
    g = Graph.__new__(Graph)
    g.graph = {'first': 1, 'second': 2, 'third': 3}
    result = g.nodes()
    assert result == list(g.graph.keys())
