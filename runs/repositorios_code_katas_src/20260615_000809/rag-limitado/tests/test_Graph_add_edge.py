from repositorios.code_katas.src.flight_graph import Graph

# curto: happy path - edge adicionada quando ambos nós já existem
def test_add_edge_happy_path_existing_nodes():
    g = Graph()
    g.add_node("A")
    g.add_node("B")
    g.add_edge("A", "B", weight=5)
    assert "A" in g.graph and "B" in g.graph["A"]
    assert g.graph["A"]["B"] == 5

# curto: cria node2 quando não existente
def test_add_edge_creates_node2_when_missing():
    g = Graph()
    g.add_node("A")
    g.add_edge("A", "B", weight=3)
    assert "B" in g.graph
    assert g.graph["A"]["B"] == 3

# curto: cria node1 quando não existente
def test_add_edge_creates_node1_when_missing():
    g = Graph()
    g.add_node("B")
    g.add_edge("A", "B", weight=9)
    assert "A" in g.graph
    assert g.graph["A"]["B"] == 9

# curto: edge existente não é sobrescrito
def test_add_edge_existing_weight_not_overwritten():
    g = Graph()
    g.add_node("A")
    g.add_node("B")
    g.add_edge("A", "B", weight=3)
    g.add_edge("A", "B", weight=6)
    assert g.graph["A"]["B"] == 3
