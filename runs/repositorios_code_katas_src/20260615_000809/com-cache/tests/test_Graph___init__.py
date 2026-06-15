from repositorios.code_katas.src.flight_graph import Graph

# Verifica inicialização feliz: cria uma instância e verifica que graph é um dict vazio
def test_init_creates_empty_graph_dict():
    g = Graph()
    assert isinstance(g.graph, dict)
    assert g.graph == {}

# Verifica que duas instâncias possuem dicionários independentes
def test_init_graphs_are_independent():
    g1 = Graph()
    g2 = Graph()
    assert g1.graph is not g2.graph
    assert g1.graph == {}
    assert g2.graph == {}
