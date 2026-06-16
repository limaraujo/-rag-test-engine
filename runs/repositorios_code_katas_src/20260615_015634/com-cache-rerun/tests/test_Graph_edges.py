from repositorios.code_katas.src.flight_graph import Graph

# curto: caminho feliz - grafo vazio retorna lista vazia
def test_edges_empty_graph():
    g = Graph()
    assert g.edges() == []

# curto: caminho feliz - grafo com uma aresta gera entradas para A e B
def test_edges_single_edge():
    g = Graph()
    g.add_edge("A", "B", weight=1)
    assert g.edges() == ["A: ['B']", "B: []"]

# curto: caminho feliz - múltiplas arestas a partir do mesmo nó gera entradas para A, B, C
def test_edges_multiple_edges_from_same_node():
    g = Graph()
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    assert g.edges() == ["A: ['B', 'C']", "B: []", "C: []"]
