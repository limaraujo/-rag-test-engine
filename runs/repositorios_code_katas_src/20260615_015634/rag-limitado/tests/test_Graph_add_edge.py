from repositorios.code_katas.src.flight_graph import Graph

# happy path: node1 ausente, node2 existente; aresta criada com peso
def test_add_edge_creates_missing_node1_and_sets_weight_when_node2_present():
    g = Graph()
    g.add_node("B")
    g.add_edge("A", "B", weight=2)
    assert "A" in g.graph
    assert g.graph["A"]["B"] == 2
    assert "B" in g.graph

# branch: node2 ausente; cria node2 e adiciona aresta
def test_add_edge_creates_missing_node2_when_node1_present():
    g = Graph()
    g.add_node("A")
    g.add_edge("A", "C", weight=5)
    assert "A" in g.graph
    assert g.graph["A"]["C"] == 5
    assert "C" in g.graph

# branch: aresta já existente não reescreve o peso
def test_add_edge_existing_edge_not_overwritten():
    g = Graph()
    g.add_edge("A", "D", weight=4)
    assert g.graph["A"]["D"] == 4
    g.add_edge("A", "D", weight=8)
    assert g.graph["A"]["D"] == 4
