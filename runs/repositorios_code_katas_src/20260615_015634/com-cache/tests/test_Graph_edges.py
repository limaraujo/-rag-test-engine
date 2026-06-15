from repositorios.code_katas.src.flight_graph import Graph

# curto: caminho feliz - grafo vazio retorna lista vazia
def test_edges_empty_graph():
    g = Graph()
    assert g.edges() == []

# curto: caminho feliz - grafo com uma aresta gera entradas para A e B
def test_edges_single_edge():
    g = Graph()
    g.add_edge("A", "B", weight=3)
    assert g.edges() == ["A: ['B']", "B: []"]

# curto: caminho feliz - múltiplas arestas de A para B e C
def test_edges_multiple_edges():
    g = Graph()
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    assert g.edges() == ["A: ['B', 'C']", "B: []", "C: []"]
