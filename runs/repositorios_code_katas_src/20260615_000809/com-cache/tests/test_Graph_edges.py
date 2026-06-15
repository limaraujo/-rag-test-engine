from repositorios.code_katas.src.flight_graph import Graph

# testa caminho feliz: um único edge gera a estrutura esperada
def test_edges_happy_path_single_edge():
    g = Graph()
    g.add_edge("A", "B")
    assert g.edges() == ["A: ['B']", "B: []"]

# testa caso de borda: grafo sem arestas
def test_edges_empty_graph():
    g = Graph()
    assert g.edges() == []

# testa múltiplas arestas e ordem de leitura
def test_edges_multiple_edges_order_and_neighbors():
    g = Graph()
    g.add_edge("X", "Y")
    g.add_edge("X", "Z")
    assert g.edges() == ["X: ['Y', 'Z']", "Y: []", "Z: []"]
