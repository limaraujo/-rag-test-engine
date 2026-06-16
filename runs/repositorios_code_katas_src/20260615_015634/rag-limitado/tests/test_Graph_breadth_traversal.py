import pytest
from repositorios.code_katas.src.flight_graph import Graph


# teste feliz: mapa simples com A -> B, C; B -> D; C -> E; verifica ordem BFS
def test_breadth_traversal_happy_path_order():
    g = Graph.__new__(Graph)
    g.graph = {
        "A": {"B": {}, "C": {}},
        "B": {"D": {}},
        "C": {"E": {}},
        "D": {},
        "E": {},
    }
    assert g.breadth_traversal("A") == ["A", "B", "C", "D", "E"]

# teste de ciclo: garante que não há loop infinito e visita apenas cada nó uma vez
def test_breadth_traversal_cycle_stops_at_three():
    g = Graph.__new__(Graph)
    g.graph = {
        "A": {"B": {}, "C": {}},
        "B": {"C": {}},
        "C": {"A": {}},
    }
    assert g.breadth_traversal("A") == ["A", "B", "C"]

# teste de exceção: iniciar em nó ausente deve levantar KeyError
def test_breadth_traversal_missing_start_raises_keyerror():
    g = Graph.__new__(Graph)
    g.graph = {"X": {}}
    with pytest.raises(KeyError):
        g.breadth_traversal("Y")

# teste de caminhos duplicados: verifica que duplicates no node_list não quebram a travessia
def test_breadth_traversal_duplicate_path_handling():
    g = Graph.__new__(Graph)
    g.graph = {
        "A": {"B": {}, "C": {}},
        "B": {"C": {}},
        "C": {},
    }
    assert g.breadth_traversal("A") == ["A", "B", "C"]
