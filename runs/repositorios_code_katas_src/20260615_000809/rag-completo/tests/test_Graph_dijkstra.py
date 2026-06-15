from repositorios.code_katas.src.flight_graph import Graph

# happy path: verifica caminho mais curto entre A e D (A->B->D)
def test_dijkstra_happy_path_basic():
    g = Graph()
    g.add_node('A')
    g.add_node('B')
    g.add_node('C')
    g.add_node('D')
    g.add_edge('A', 'B', 1)
    g.add_edge('A', 'C', 4)
    g.add_edge('B', 'D', 2)
    g.add_edge('C', 'D', 1)

    result = g.dijkstra('A', 'D')
    assert result == {3: ['A', 'B', 'D']}

# start equals finish: verifica retorno para start == finish
def test_dijkstra_start_equals_finish():
    g = Graph()
    g.add_node('X')

    result = g.dijkstra('X', 'X')
    assert result == {0: ['X']}

# unreachable: verifica None quando finish não é alcançável
def test_dijkstra_unreachable():
    g = Graph()
    g.add_node('A')
    g.add_node('B')
    g.add_node('C')
    g.add_edge('A', 'B', 1)

    result = g.dijkstra('A', 'C')
    assert result is None

# with cycle: verifica caminho correto mesmo com ciclos (A->B->C vs A->C)
def test_dijkstra_with_cycle_and_shortest_path():
    g = Graph()
    g.add_node('A')
    g.add_node('B')
    g.add_node('C')
    g.add_edge('A', 'B', 1)
    g.add_edge('B', 'A', 1)  # ciclo
    g.add_edge('B', 'C', 2)
    g.add_edge('A', 'C', 4)

    result = g.dijkstra('A', 'C')
    assert result == {3: ['A', 'B', 'C']}
