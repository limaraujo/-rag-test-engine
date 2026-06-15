from repositorios.code_katas.src.flight_graph import Graph

# happy path: Graph.__init__ cria grafo interno vazio
def test_init_sets_empty_graph():
    g = Graph()
    assert isinstance(g.graph, dict)
    assert g.graph == {}

# edge case: grafos de diferentes instâncias são independentes
def test_init_instances_are_independent():
    g1 = Graph()
    g2 = Graph()
    assert g1.graph is not g2.graph
    g1.graph['A'] = {}
    assert 'A' not in g2.graph
