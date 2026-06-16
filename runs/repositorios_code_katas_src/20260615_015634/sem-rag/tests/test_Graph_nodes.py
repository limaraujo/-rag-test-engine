from repositorios.code_katas.src.flight_graph import Graph

# Test 1: happy path with multiple nodes, preserves insertion order
def test_nodes_happy_path_preserves_order():
    g = Graph()
    g.graph = {"A": {}, "B": {}, "C": {}}
    assert g.nodes() == ["A", "B", "C"]

# Test 2: edge case - empty graph returns empty list
def test_nodes_empty_graph_returns_empty_list():
    g = Graph()
    g.graph = {}
    assert g.nodes() == []

# Test 3: numeric node keys preserve order
def test_nodes_preserves_numeric_order():
    g = Graph()
    g.graph = {1: {"val": 1}, 2: {"val": 2}}
    assert g.nodes() == [1, 2]
