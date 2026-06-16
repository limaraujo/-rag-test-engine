from collections import OrderedDict
from repositorios.code_katas.src.trietree import TrieNode

# Verifica construtor padrão: valor None e children vazia
def test_trienode_default_constructor():
    node = TrieNode()
    assert node.value is None
    assert isinstance(node.children, OrderedDict)
    assert len(node.children) == 0

# Verifica atribuição de valor passado no construtor
def test_trienode_value_assignment():
    node = TrieNode(value=123)
    assert node.value == 123
    assert isinstance(node.children, OrderedDict)
    assert len(node.children) == 0

# Verifica que children inicia como OrderedDict vazio mesmo com valor fornecido
def test_trienode_children_empty_on_init_with_value():
    node = TrieNode(value="X")
    assert isinstance(node.children, OrderedDict)
    assert len(node.children) == 0
