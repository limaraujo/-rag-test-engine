from repositorios.code_katas.src.flight_graph import Graph

# Testa se has_node retorna True quando o nó está presente (happy path)
def test_has_node_true_when_node_present():
    g = Graph()
    g.graph = {'A': 1, 'B': 2}
    assert g.has_node('A') is True

# Testa se has_node retorna False quando o nó não está presente (caso de ausência)
def test_has_node_false_when_node_missing():
    g = Graph()
    g.graph = {'A': 1, 'B': 2}
    assert g.has_node('C') is False

# Testa se has_node retorna False para grafo vazio (caso de borda)
def test_has_node_false_on_empty_graph():
    g = Graph()
    g.graph = {}
    assert g.has_node('A') is False

# Testa comportamento para candidato não-hashable não existente nos nós (caso de borda)
def test_has_node_with_unhashable_candidate_returns_false():
    g = Graph()
    g.graph = {'A': 1}
    assert g.has_node(['A']) is False
