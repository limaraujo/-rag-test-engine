from repositorios.code_katas.src.flight_graph import Graph

# Testa add_edge com ambos os nós ausentes (caminho feliz)
def test_add_edge_creates_both_nodes_and_edge_when_missing():
    g = Graph()
    g.add_edge("A", "B")
    assert "A" in g.graph
    assert "B" in g.graph
    assert g.graph["A"]["B"] == 0

# Testa add_edge quando o nó1 existe e o nó2 não (cria nó2)
def test_add_edge_creates_missing_node2_when_node1_exists():
    g = Graph()
    g.add_node("A")
    g.add_edge("A", "B", weight=3)
    assert "A" in g.graph and "B" in g.graph
    assert g.graph["A"]["B"] == 3

# Testa add_edge não sobrescreve edge existente
def test_add_edge_does_not_overwrite_existing_edge():
    g = Graph()
    g.add_edge("A", "B", weight=7)
    g.add_edge("A", "B", weight=99)
    assert g.graph["A"]["B"] == 7

# Testa add_edge quando ambos os nós existem e a aresta não existe (usa peso informado)
def test_add_edge_when_nodes_exist_without_edge_sets_given_weight():
    g = Graph()
    g.add_node("A")
    g.add_node("B")
    g.add_edge("A", "B", weight=4)
    assert g.graph["A"]["B"] == 4
