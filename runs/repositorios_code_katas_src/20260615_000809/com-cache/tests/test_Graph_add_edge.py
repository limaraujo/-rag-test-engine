from repositorios.code_katas.src.flight_graph import Graph

# Teste 'caminho feliz': ambos nós não existem; cria nós e aresta com peso especificado
def test_add_edge_happy_path_both_nodes_missing():
    g = Graph()
    g.add_edge("A", "B", weight=7)
    assert "A" in g.graph and "B" in g.graph
    assert g.graph["A"]["B"] == 7

# Teste 'node1 existente, node2 ausente': verifica que node2 é criado e edge é adicionada com peso
def test_add_edge_node1_exists_node2_missing():
    g = Graph()
    g.add_node("A")
    g.add_edge("A", "C", weight=3)
    assert "C" in g.graph
    assert g.graph["A"]["C"] == 3

# Teste 'edge já existe não é sobrescrita': assegura que peso não muda em segunda chamada
def test_add_edge_existing_edge_not_overwritten():
    g = Graph()
    g.add_edge("X", "Y", weight=5)
    g.add_edge("X", "Y", weight=99)
    assert g.graph["X"]["Y"] == 5
