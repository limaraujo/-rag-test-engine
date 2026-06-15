from repositorios.code_katas.src.flight_graph import Graph

def _make_graph_with_keys(keys):
    g = Graph.__new__(Graph)  # bypass __init__
    g.graph = dict.fromkeys(keys, None)
    return g

# happy path: node present in the graph
def test_has_node_happy_path_present():
    g = _make_graph_with_keys(['a', 'b', 'c'])
    assert g.has_node('b') is True

# edge case: node not present in the graph
def test_has_node_absent_returns_false():
    g = _make_graph_with_keys(['x', 'y'])
    assert g.has_node('z') is False

# dynamic update: after modifying the graph, has_node reflects new keys
def test_has_node_updates_with_graph_change():
    g = _make_graph_with_keys(['a'])
    assert g.has_node('a') is True
    g.graph['b'] = 2
    assert g.has_node('b') is True
