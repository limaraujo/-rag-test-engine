import pytest
from repositorios.code_katas.src.flight_graph import Graph

# Teste: happy path - remover nó existente e limpar arestas inbound de outros nós
def test_del_node_happy_path_removes_node_and_inbound_edges():
    g = Graph()
    g.add_node('A')
    g.add_node('B')
    g.add_node('C')
    g.graph['A']['B'] = True
    g.graph['C']['B'] = True
    g.graph['B'] = {'C': True}  # edges of B (outgoing) para cobrir removimento de entradas
    g.del_node('B')
    assert 'B' not in g.graph
    assert 'B' not in g.graph['A']
    assert 'B' not in g.graph['C']
    assert 'C' in g.graph

# Teste: exceção ao tentar deletar nó que não existe (branch de erro)
def test_del_node_missing_key_raises():
    g = Graph()
    g.add_node('A')
    with pytest.raises(KeyError):
        g.del_node('B')

# Teste: nó alvo sem entradas inbound (branch do loop não executa deleção)
def test_del_node_with_no_inbound_edges():
    g = Graph()
    g.add_node('A')
    g.add_node('B')
    g.graph['B'] = {}  # B existe mas não há arestas inbound para B
    g.del_node('B')
    assert 'B' not in g.graph
    assert 'A' in g.graph
