from collections import OrderedDict
from repositorios.code_katas.src.trietree import TrieNode


# Teste feliz: construção padrão cria valor None e children vazia
def test_trienode_default_constructor():
    node = TrieNode()
    assert node.value is None
    assert isinstance(node.children, OrderedDict)
    assert len(node.children) == 0


# Teste feliz: construção com valor específico
def test_trienode_constructor_with_value():
    val = 'x'
    node = TrieNode(val)
    assert node.value == val
    assert isinstance(node.children, OrderedDict)
    assert len(node.children) == 0


# Teste de borda / independência entre instâncias
def test_trienode_children_mutation_per_instance():
    a = TrieNode('a')
    b = TrieNode('b')
    a.children['child'] = TrieNode('c')
    assert 'child' in a.children
    assert len(a.children) == 1
    assert len(b.children) == 0


# Teste de tipo de children permanece consistente
def test_trienode_children_type_consistency():
    n = TrieNode()
    assert type(n.children) is OrderedDict
    n.children['k'] = TrieNode('v')
    assert isinstance(n.children, OrderedDict)
    assert list(n.children.keys()) == ['k']
