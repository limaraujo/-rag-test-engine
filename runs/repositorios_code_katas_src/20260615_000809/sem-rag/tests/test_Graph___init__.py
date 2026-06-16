from repositorios.code_katas.src.flight_graph import Graph

# Verifica que o construtor cria um atributo graph como dicionário vazio (caso feliz)
def test_init_sets_empty_graph_dict():
    g = Graph()
    assert isinstance(g.graph, dict)
    assert g.graph == {}

# Verifica que instâncias diferentes possuem dicionários graph distintos (independência entre instâncias)
def test_init_independent_graphs():
    g1 = Graph()
    g2 = Graph()
    assert g1.graph is not g2.graph
    assert g1.graph == {}
    assert g2.graph == {}

# Verifica que modificar graph de uma instância não afeta a outra (invariância de instâncias)
def test_mutation_isolated_per_instance():
    g1 = Graph()
    g2 = Graph()
    g1.graph['a'] = 1
    assert g1.graph != g2.graph
    assert g2.graph == {}
