from repositorios.code_katas.src.flight_graph import Graph

# curto: verifica que retorna True quando o nó está presente (caminho feliz)
def test_has_node_true_present():
    g = object.__new__(Graph)
    g.graph = {'A': {}, 'B': {}}
    assert g.has_node('A') is True

# curto: verifica que retorna False quando o nó não está presente
def test_has_node_false_absent():
    g = object.__new__(Graph)
    g.graph = {'A': {}, 'B': {}}
    assert g.has_node('C') is False
