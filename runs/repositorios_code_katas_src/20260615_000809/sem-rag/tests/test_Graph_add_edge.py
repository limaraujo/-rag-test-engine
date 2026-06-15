from repositorios.code_katas.src.flight_graph import Graph

# happy path: ambos os nós ausentes -> adiciona aresta e cria nós
def test_add_edge_both_nodes_missing_creates_nodes_and_edge():
    g = Graph()
    g.add_edge('A', 'B', weight=5)
    assert 'A' in g.graph and 'B' in g.graph
    assert g.graph['A']['B'] == 5

# branch: nó1 existente, nó2 ausente
def test_add_edge_missing_destination_node_only():
    g = Graph()
    g.add_node('A')
    g.add_edge('A', 'B', weight=4)
    assert g.graph['A']['B'] == 4
    assert 'B' in g.graph

# branch: aresta já existente mantém peso
def test_add_edge_existing_edge_preserves_weight():
    g = Graph()
    g.graph['A'] = {'B': 7}
    g.add_edge('A', 'B', weight=3)
    assert g.graph['A']['B'] == 7

# default: peso default 0 quando não informado
def test_add_edge_defaults_weight_zero():
    g = Graph()
    g.add_edge('M', 'N')
    assert g.graph['M']['N'] == 0
