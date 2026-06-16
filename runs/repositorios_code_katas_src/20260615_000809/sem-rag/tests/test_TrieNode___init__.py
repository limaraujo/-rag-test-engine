from collections import OrderedDict
from repositorios.code_katas.src.trietree import TrieNode

# happy path: verifica valor fornecido e children inicial vazio
def test_init_sets_value_and_empty_children_happy_path():
    node = TrieNode(value=5)
    assert node.value == 5
    assert isinstance(node.children, OrderedDict)
    assert len(node.children) == 0

# borda: valor padrão None e children inicial vazio
def test_init_default_value_none_and_empty_children():
    node = TrieNode()
    assert node.value is None
    assert isinstance(node.children, OrderedDict)
    assert len(node.children) == 0

# isolamento de estruturas: diferentes nós possuem dicionários de children distintos
def test_each_node_has_independent_children_dict():
    node1 = TrieNode('a')
    node2 = TrieNode(None)
    node1.children['x'] = TrieNode(3)
    assert 'x' in node1.children
    assert 'x' not in node2.children
