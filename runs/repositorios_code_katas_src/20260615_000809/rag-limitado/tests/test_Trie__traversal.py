from collections import OrderedDict
import pytest
from repositorios.code_katas.src.trietree import Trie

class DummyNode:
    def __init__(self):
        self.children = OrderedDict()

# Verifica caminho feliz: múltiplos níveis são visitados e a ordem é preservada (first=True)
def test_traversal_happy_path_multiple_levels_first_true():
    trie = Trie()
    root = DummyNode()
    nodeA = DummyNode()
    nodeB = DummyNode()

    root.children['A'] = nodeA
    root.children['$'] = DummyNode()
    nodeA.children['B'] = nodeB
    nodeA.children['$'] = DummyNode()

    result = list(trie._traversal(root, first=True))
    assert result == [nodeA, nodeB]

# Verifica que '$' é ignorado (end marker) corretamente
def test_traversal_skips_end_marker_key():
    trie = Trie()
    root = DummyNode()
    root.children['$'] = DummyNode()

    result = list(trie._traversal(root, first=True))
    assert result == []

# Verifica ordem em várias ramificações (branching)
def test_traversal_multiple_branches_order():
    trie = Trie()
    root = DummyNode()
    nodeA = DummyNode()
    nodeC = DummyNode()
    nodeD = DummyNode()

    root.children['A'] = nodeA
    root.children['C'] = nodeC
    root.children['$'] = DummyNode()
    nodeA.children['D'] = nodeD
    nodeA.children['$'] = DummyNode()

    result = list(trie._traversal(root, first=True))
    assert result == [nodeA, nodeD, nodeC]

# Verifica que quando first=False o próprio nó é yieldado (inclui root)
def test_traversal_includes_root_when_started_with_false():
    trie = Trie()
    root = DummyNode()
    nodeA = DummyNode()

    root.children['A'] = nodeA
    root.children['$'] = DummyNode()

    result = list(trie._traversal(root, first=False))
    assert result == [root, nodeA]
