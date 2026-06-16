from repositorios.code_katas.src.flight_graph import Graph

# curto: caminho feliz - grafo vazio retorna lista vazia
def test_nodes_empty_graph():
    g = Graph()
    assert g.nodes() == []

# curto: caminho feliz - a ordem de inserção de nós é mantida em nodes()
def test_nodes_insertion_order_preserved():
    g = Graph()
    g.add_node("A")
    g.add_node("B")
    g.add_node("C")
    assert g.nodes() == ["A", "B", "C"]

# curto: quando adiciona aresta com nós ausentes, os nós são criados na ordem de inserção e refletem em nodes()
def test_nodes_created_by_add_edge_order():
    g = Graph()
    g.add_edge("A", "B", weight=3)
    assert "A" in g.graph and "B" in g.graph
    assert g.nodes() == ["A", "B"]
