from repositorios.code_katas.src.flight_graph import Graph

# Verifica o caminho feliz com múltiplos nós e vizinhos mantendo a ordem de inserção
def test_edges_happy_path_multiple_nodes():
    g = Graph()
    g.graph = {'A': {'B': {}, 'C': {}}, 'B': {'A': {}}, 'C': {}}
    assert g.edges() == ["A: ['B', 'C']", "B: ['A']", "C: []"]

# Verifica o comportamento para grafo vazio (sem nós)
def test_edges_empty_graph():
    g = Graph()
    g.graph = {}
    assert g.edges() == []

# Verifica o nó único sem arestas, formato correto
def test_edges_single_node_no_edges():
    g = Graph()
    g.graph = {'X': {}}
    assert g.edges() == ["X: []"]
