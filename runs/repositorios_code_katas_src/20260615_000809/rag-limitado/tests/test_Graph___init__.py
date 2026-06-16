from repositorios.code_katas.src.flight_graph import Graph

# curto: happy path: Graph() cria graph como dict vazio
def test_init_creates_empty_graph_dict():
    g = Graph()
    assert isinstance(g.graph, dict)
    assert g.graph == {}

# curto: isola os estados entre instâncias: grafos independentes
def test_init_instances_have_independent_graphs():
    g1 = Graph()
    g2 = Graph()
    assert g1.graph is not g2.graph
    assert g1.graph == {}
    assert g2.graph == {}
