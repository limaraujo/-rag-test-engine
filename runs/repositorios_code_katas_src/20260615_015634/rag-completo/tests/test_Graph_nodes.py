from repositorios.code_katas.src.flight_graph import Graph

# Verifica o caminho feliz: mantém a ordem de inserção das chaves do grafo
def test_nodes_happy_path_preserves_order():
    g = Graph()
    g.graph = {'A': {'B': 1}, 'C': {'A': 2}, 'B': {}}
    assert g.nodes() == ['A', 'C', 'B']

# Verifica o caso de borda: grafo sem nós retorna lista vazia
def test_nodes_empty_graph_returns_empty_list():
    g = Graph()
    g.graph = {}
    assert g.nodes() == []

# Verifica suporte a chaves não-strings e preservação de ordem
def test_nodes_preserves_numeric_keys_order():
    g = Graph()
    g.graph = {1: {}, 2: {}, 3: {}}
    assert g.nodes() == [1, 2, 3]
