from repositorios.code_katas.src.flight_graph import Graph

# Verifica caminho mais curto simples (caso feliz: múltiplos passos)
def test_dijkstra_happy_path_basic():
    g = Graph()
    graph = {
        'A': {'B': 1, 'C': 4},
        'B': {'C': 2, 'D': 5},
        'C': {'D': 1},
        'D': {}
    }
    g.graph = graph
    g.nodes = lambda: list(graph.keys())
    assert g.dijkstra('A', 'D') == {4: ['A', 'B', 'C', 'D']}

# Verifica caminho direto de A a D quando há apenas esse caminho
def test_dijkstra_direct_edge_finish():
    g = Graph()
    graph = {
        'A': {'D': 2},
        'D': {}
    }
    g.graph = graph
    g.nodes = lambda: list(graph.keys())
    assert g.dijkstra('A', 'D') == {2: ['A', 'D']}

# Verifica comportamento quando finish é inalcançável (retorna None)
def test_dijkstra_unreachable_finish():
    g = Graph()
    graph = {
        'A': {'B': 2},
        'B': {},
        'C': {}
    }
    g.graph = graph
    g.nodes = lambda: list(graph.keys())
    assert g.dijkstra('A', 'C') is None

# Verifica escolha da rota mais curta entre múltiplas opções
# Nessa configuração, A->C->D é mais eficiente que A->B->D
def test_dijkstra_shortest_path_choice():
    g = Graph()
    graph = {
        'A': {'B': 1, 'C': 1},
        'B': {'D': 2},
        'C': {'D': 1},
        'D': {}
    }
    g.graph = graph
    g.nodes = lambda: list(graph.keys())
    assert g.dijkstra('A', 'D') == {2: ['A', 'C', 'D']}
