from repositorios.code_katas.src.flight_graph import Graph

# happy path: dois nós com arestas
def test_edges_happy_path_multiple_nodes():
    g = Graph()
    g.graph = {'A': {'B': {}, 'C': {}}, 'D': {}}
    assert g.edges() == ["A: ['B', 'C']", "D: []"]

# borda: nó único sem arestas
def test_edges_single_node_no_edges():
    g = Graph()
    g.graph = {'Z': {}}
    assert g.edges() == ["Z: []"]

# caso simples: nó com uma aresta
def test_edges_single_node_with_one_edge():
    g = Graph()
    g.graph = {'X': {'Y': {}}}
    assert g.edges() == ["X: ['Y']"]

# caso vazio: grafo sem nós
def test_edges_empty_graph():
    g = Graph()
    g.graph = {}
    assert g.edges() == []
