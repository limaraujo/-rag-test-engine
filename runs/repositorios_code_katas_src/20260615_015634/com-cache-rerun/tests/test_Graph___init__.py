from repositorios.code_katas.src.flight_graph import Graph

# Teste curto: __init__ cria grafo interno como dict vazio (happy path)
def test_init_sets_empty_graph():
    g = Graph()
    assert isinstance(g.graph, dict)
    assert g.graph == {}

# Teste curto: instâncias do Graph são independentes (edge case: isolamento entre instâncias)
def test_init_instances_are_independent():
    g1 = Graph()
    g2 = Graph()
    assert g1.graph is not g2.graph
    assert g1.graph == {}
    assert g2.graph == {}
