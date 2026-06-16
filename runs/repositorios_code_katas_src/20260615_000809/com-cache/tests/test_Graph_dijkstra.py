import pytest
from repositorios.code_katas.src.flight_graph import Graph

# verifica caminho mais curto (happy path, caminho único)
def test_dijkstra_happy_path_unique_shortest():
    g = Graph()
    g.add_edge('A', 'B', 1)
    g.add_edge('B', 'D', 2)
    g.add_edge('A', 'C', 4)
    g.add_edge('C', 'D', 1)
    result = g.dijkstra('A', 'D')
    assert result == {3: ['A', 'B', 'D']}

# verifica comportamento quando o destino não é alcançável (caminho ausente)
def test_dijkstra_unreachable_finish_returns_none():
    g = Graph()
    g.add_edge('A', 'B', 3)
    result = g.dijkstra('A', 'D')
    assert result is None

# verifica caso em que start == finish (retorna caminho trivial)
def test_dijkstra_start_equals_finish_returns_trivial_path():
    g = Graph()
    g.add_edge('A', 'B', 5)
    result = g.dijkstra('A', 'A')
    assert result == {0: ['A']}

# verifica caminho com várias etapas (constrói caminho A->B->C)
def test_dijkstra_happy_path_multiple_steps():
    g = Graph()
    g.add_edge('A', 'B', 2)
    g.add_edge('B', 'C', 2)
    g.add_edge('A', 'C', 10)
    result = g.dijkstra('A', 'C')
    assert result == {4: ['A', 'B', 'C']}
