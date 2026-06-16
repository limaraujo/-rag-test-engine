from repositorios.code_katas.src.flight_graph import Graph

# curto: caminho feliz - ambos os nós não existem; aresta criada com peso especificado
def test_add_edge_creates_missing_nodes_and_edge():
    g = Graph()
    g.add_edge("A", "B", weight=3)
    assert "A" in g.graph
    assert "B" in g.graph
    assert g.graph["A"]["B"] == 3

# curto: caminho feliz - aresta existente não é sobrescrita
def test_add_edge_does_not_overwrite_existing_edge():
    g = Graph()
    g.add_node("A")
    g.add_node("B")
    g.graph["A"]["B"] = 3
    g.add_edge("A", "B", weight=10)
    assert g.graph["A"]["B"] == 3

# curto: caminho feliz - apenas node1 existente; node2 é criado e aresta é adicionada
def test_add_edge_creates_node2_when_only_node1_exists():
    g = Graph()
    g.add_node("A")
    g.add_edge("A", "B", weight=7)
    assert "B" in g.graph
    assert g.graph["A"]["B"] == 7
