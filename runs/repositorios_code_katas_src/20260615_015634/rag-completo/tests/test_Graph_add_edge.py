from repositorios.code_katas.src.flight_graph import Graph

# curto: happy path - ambos nós inexistentes; cria nós e a aresta
def test_add_edge_both_missing_creates_nodes_and_edge():
    g = Graph()
    g.add_edge("A", "B", weight=3)
    assert "A" in g.graph
    assert "B" in g.graph
    assert g.graph["A"]["B"] == 3

# curto: caso em que a aresta já existe; o peso não deve ser sobrescrito
def test_add_edge_existing_edge_not_overwritten():
    g = Graph()
    g.add_edge("A", "B", weight=5)
    g.add_edge("A", "B", weight=99)
    assert g.graph["A"]["B"] == 5

# curto: Node1 existente, Node2 ausente; deve criar Node2 e adicionar aresta com o peso correto
def test_add_edge_node1_exists_node2_missing_creates_edge():
    g = Graph()
    g.add_node("A")
    g.add_edge("A", "C", weight=7)
    assert "A" in g.graph and "C" in g.graph
    assert g.graph["A"]["C"] == 7

# curto: ambos existindo, sem aresta anterior; deve criar a aresta com o peso informado
def test_add_edge_both_exist_no_edge_creates_edge():
    g = Graph()
    g.add_node("A")
    g.add_node("B")
    g.add_edge("A", "B", weight=4)
    assert g.graph["A"]["B"] == 4
