import collections
from repositorios.code_katas.src.trietree import Trie

class DummyTrie(Trie):
    def __init__(self):
        pass

class FakeNode:
    def __init__(self, children=None):
        self.children = collections.OrderedDict(children or [])

# Verifica travessia em árvore vazia: retorna lista vazia
def test_traversal_empty_tree():
    root = FakeNode([])
    trie = DummyTrie()
    assert list(trie._traversal(root, first=True)) == []

# Verifica caminho feliz com apenas um filho
def test_traversal_single_child():
    child = FakeNode([])
    root = FakeNode([('a', child)])
    trie = DummyTrie()
    assert list(trie._traversal(root, first=True)) == [child]

# Verifica travessia com múltiplos níveis (pre-order): yields internals then leaves
def test_traversal_multiple_levels():
    leaf = FakeNode([])
    middle = FakeNode([('c', leaf)])
    node_b = FakeNode([])
    root = FakeNode([('a', middle), ('b', node_b)])
    trie = DummyTrie()
    assert list(trie._traversal(root, first=True)) == [middle, leaf, node_b]

# Verifica que '$' é ignorado como chave de nível: não inclui os nós sob '$'
def test_traversal_ignores_dollar_keys():
    dollar = FakeNode([])
    node_a = FakeNode([])
    root = FakeNode([('$', dollar), ('a', node_a)])
    trie = DummyTrie()
    assert list(trie._traversal(root, first=True)) == [node_a]
