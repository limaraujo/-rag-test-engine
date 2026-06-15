from repositorios.code_katas.src.flight_graph import Graph

# curto: caminho feliz - grafo vazio retorna lista vazia
def test_nodes_empty_graph():
    g = Graph()
    assert g.nodes() == []

# curto: caminho feliz - nós são adicionados ao adicionar arestas
def test_nodes_after_edges_insertion():
    g = Graph()
    g.add_edge("A","B")
    g.add_edge("B","C")
    assert set(g.nodes()) == {"A","B","C"}

# curto: caminho feliz - grafo com múltiplos componentes produz nós de todos os componentes
def test_nodes_multiple_components():
    g = Graph()
    g.add_edge("A","B")
    g.add_edge("C","D")
    g.add_edge("E","F")
    assert set(g.nodes()) == {"A","B","C","D","E","F"}
