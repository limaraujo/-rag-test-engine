import pytest
from repositorios.code_katas.src.trietree import Trie

class DummyNode:
    def __init__(self):
        self.children = {}

# happy path: remove a word that is a leaf with no bifurcation at root
def test_remove_happy_path_leaf_no_bifurcation():
    # breve: setup trie with root -> 'a' -> '$'
    trie = object.__new__(Trie)
    trie.root = DummyNode()
    trie._size = 1
    node_a = DummyNode()
    node_a.children['$'] = DummyNode()
    trie.root.children['a'] = node_a

    trie.remove("a")

    assert trie.root.children == {}
    assert '$' not in (trie.root.children.get('a', DummyNode()).children)
    assert trie._size == 1

# branch: remove when a bifurcation occurs earlier in the path
def test_remove_with_bifurcation_removes_branch():
    # setup: root has 'a' and 'x'; path 'a' -> 'b' -> '$'
    trie = object.__new__(Trie)
    trie.root = DummyNode()
    trie._size = 2
    root_a = DummyNode()
    root_x = DummyNode()
    trie.root.children['x'] = root_x
    trie.root.children['a'] = root_a

    node_b = DummyNode()
    node_b.children['$'] = DummyNode()
    root_a.children['b'] = node_b

    trie.remove("ab")

    assert 'a' not in trie.root.children
    assert 'x' in trie.root.children

# branch: remove end marker when terminal node has other branches
def test_remove_end_marker_only_when_terminal_has_other_branches():
    # setup: path 'a' -> 'b' where node 'b' has '$' and 'c'
    trie = object.__new__(Trie)
    trie.root = DummyNode()
    trie._size = 1
    root_a = DummyNode()
    node_b = DummyNode()
    node_b.children['$'] = DummyNode()
    node_b.children['c'] = DummyNode()
    root_a.children['b'] = node_b
    trie.root.children['a'] = root_a

    trie.remove("ab")

    assert '$' not in node_b.children
    assert 'a' in trie.root.children

# exception: TypeError for non-string input
def test_remove_raises_type_error_for_non_string():
    trie = object.__new__(Trie)
    trie.root = DummyNode()
    trie._size = 0
    with pytest.raises(TypeError):
        trie.remove(123)
