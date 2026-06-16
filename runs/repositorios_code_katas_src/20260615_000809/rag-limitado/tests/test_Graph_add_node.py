import pytest
from repositorios.code_katas.src.flight_graph import Graph

# Testa add_node cobrindo caminho feliz (novo nó) e exceção KeyError quando nó já existe
@pytest.mark.parametrize("initial_nodes, new_node, expect_error", [
    ([], 'A', False),
    (['A'], 'A', True),
])
def test_add_node_branches(initial_nodes, new_node, expect_error):
    g = Graph()
    for n in initial_nodes:
        g.add_node(n)
    if expect_error:
        with pytest.raises(KeyError):
            g.add_node(new_node)
    else:
        g.add_node(new_node)
        assert new_node in g.graph
        assert g.graph[new_node] == {}
