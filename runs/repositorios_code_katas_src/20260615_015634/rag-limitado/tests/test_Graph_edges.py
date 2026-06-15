from repositorios.code_katas.src.flight_graph import Graph

# Test: happy path with multiple nodes and edges; verify string formatting and order
def test_edges_happy_path_multiple_nodes_and_edges():
    g = Graph()
    g.graph = {"A": {"B": {}, "C": {}}, "B": {"A": {}}}
    assert g.edges() == ["A: ['B', 'C']", "B: ['A']"]

# Test: empty graph should return an empty list
def test_edges_empty_graph():
    g = Graph()
    g.graph = {}
    assert g.edges() == []

# Test: single node with no outgoing edges; expects a single entry with empty list
def test_edges_single_node_no_edges():
    g = Graph()
    g.graph = {"A": {}}
    assert g.edges() == ["A: []"]

# Test: ensure order of neighbors is preserved in the string representation
def test_edges_neighbor_order_preserved():
    g = Graph()
    g.graph = {"X": {"Y": 1, "Z": 2}, "Y": {}}
    assert g.edges() == ["X: ['Y', 'Z']", "Y: []"]
