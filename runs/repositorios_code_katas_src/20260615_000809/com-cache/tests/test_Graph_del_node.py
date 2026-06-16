import pytest
from repositorios.code_katas.src.flight_graph import Graph

# verifica exceção ao deletar nó que não existe (missing_key)
def test_del_node_missing_key_raises():
    g = Graph()
    g.graph = {'A': {}}
    with pytest.raises(KeyError):
        g.del_node('Z')

# verifica caminho feliz com aresta apontando para o nó a ser deletado (branch interna)
def test_del_node_existing_with_incoming_edge():
    g = Graph()
    g.graph = {'A': {'B': 1}, 'B': {}}
    g.del_node('B')
    assert g.graph == {'A': {}}  # 'B' removido de A e a própria B excluída

# verifica caminho feliz sem arestas entrando no nó a ser deletado
def test_del_node_existing_without_incoming_edges():
    g = Graph()
    g.graph = {'A': {'C': 2}, 'B': {}}
    g.del_node('B')
    assert g.graph == {'A': {'C': 2}}
