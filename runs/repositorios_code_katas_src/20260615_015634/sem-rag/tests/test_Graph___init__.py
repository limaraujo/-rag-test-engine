from repositorios.code_katas.src.flight_graph import Graph

# happy path: instantiation básica cria graph vazio (dict)
def test_init_creates_empty_graph_dict():
    g = Graph()
    assert isinstance(g.graph, dict)
    assert g.graph == {}

# independência entre instâncias: dicionários não são compartilhados
def test_multiple_instances_have_independent_graphs():
    g1 = Graph()
    g2 = Graph()
    g1.graph['A'] = 1
    assert g2.graph == {}
    assert g1.graph is not g2.graph

# mutabilidade do dicionário do grafo: é possível adicionar entradas
def test_graph_dictionary_is_mutable_and_stores_entries():
    g = Graph()
    g.graph['nodes'] = []
    assert g.graph['nodes'] == []
    assert isinstance(g.graph, dict)
