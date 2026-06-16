from repositorios.code_katas.src.flight_graph import Graph

# caminho feliz: ambos os nós não existem; aresta criada com peso especificado
def test_add_edge_creates_missing_nodes_and_edge():
    g = Graph()
    g.add_edge("A", "B", weight=3)
    assert "A" in g.graph
    assert "B" in g.graph
    assert g.graph["A"]["B"] == 3

# branch: aresta já existente não é sobrescrita
def test_add_edge_existing_edge_no_overwrite():
    g = Graph()
    g.graph = {"A": {"B": 3}, "B": {}}
    g.add_edge("A", "B", weight=99)
    assert g.graph["A"]["B"] == 3

# branch: node1 ausente é criado, aresta adicionada
def test_add_edge_creates_missing_node1_only():
    g = Graph()
    g.graph = {"B": {}}
    g.add_edge("A", "B", weight=5)
    assert "A" in g.graph
    assert g.graph["A"]["B"] == 5

# branch: node2 ausente é criado, aresta adicionada
def test_add_edge_creates_missing_node2_only():
    g = Graph()
    g.graph = {"A": {}}
    g.add_edge("A", "C", weight=7)
    assert "C" in g.graph
    assert g.graph["A"]["C"] == 7
