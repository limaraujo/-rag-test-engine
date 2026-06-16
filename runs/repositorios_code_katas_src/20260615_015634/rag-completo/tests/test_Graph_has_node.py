from repositorios.code_katas.src.flight_graph import Graph

# verifica se retorna True quando o nó está presente
def test_has_node_true_when_present():
    g = Graph.__new__(Graph)
    g.graph = {"A": [], "B": []}
    assert g.has_node("A") is True

# verifica se retorna False quando o nó não está presente
def test_has_node_false_when_absent():
    g = Graph.__new__(Graph)
    g.graph = {"A": [], "B": []}
    assert g.has_node("C") is False
