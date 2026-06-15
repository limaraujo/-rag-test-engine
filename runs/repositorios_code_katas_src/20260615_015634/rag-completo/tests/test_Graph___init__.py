from repositorios.code_katas.src.flight_graph import Graph

# curto: happy path — Graph.__init__ initializes an empty dict attribute 'graph'
def test_init_creates_empty_graph_dict():
    g = Graph()
    assert isinstance(g.graph, dict)
    assert g.graph == {}
    assert len(g.graph) == 0

# curto: isolated instances — multiple Graph objects do not share the same 'graph' dict
def test_init_instances_are_independent():
    g1 = Graph()
    g2 = Graph()
    assert g1.graph is not g2.graph
    assert g1.graph == {}
    assert g2.graph == {}
