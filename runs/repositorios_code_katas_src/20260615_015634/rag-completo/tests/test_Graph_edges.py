from repositorios.code_katas.src.flight_graph import Graph

def test_edges_happy_path_multiple_nodes():
    g = Graph()
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    edges = g.edges()
    assert edges == ["A: ['B', 'C']", "B: []", "C: []"]

def test_edges_empty_graph_returns_empty_list():
    g = Graph()
    assert g.edges() == []
