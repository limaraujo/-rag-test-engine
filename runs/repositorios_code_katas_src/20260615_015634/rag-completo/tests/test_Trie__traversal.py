import pytest
from repositorios.code_katas.src.trietree import Trie

# helper dummy node to simulate TrieNode-like structure for testing _traversal
class DummyNode:
    def __init__(self, value=None, children=None):
        self.value = value
        self.children = {} if children is None else children


# Test 1: Verifica que '$' é ignorado e a travessia recursiva ocorre corretamente (first=True)
def test__traversal_skips_dollar_and_recurses_first_true():
    root = DummyNode(value="root")
    a = DummyNode(value="A")
    a1 = DummyNode(value="A1")
    b = DummyNode(value="B")
    dollar = DummyNode(value="end")

    root.children = {"a": a, "$": dollar, "b": b}
    a.children = {"a1": a1}
    b.children = {}

    t = Trie()
    result = list(t._traversal(root, first=True))
    assert [node.value for node in result] == ["A", "A1", "B"]

# Test 2: Verifica que ao iniciar com first=False, a raiz é incluída na saída e a ordem DFS permanece
def test__traversal_includes_root_when_first_false():
    root = DummyNode(value="root")
    a = DummyNode(value="A")
    a1 = DummyNode(value="A1")
    b = DummyNode(value="B")
    dollar = DummyNode(value="end")

    root.children = {"a": a, "$": dollar, "b": b}
    a.children = {"a1": a1}
    b.children = {}

    t = Trie()
    result = list(t._traversal(root, first=False))
    assert [node.value for node in result] == ["root", "A", "A1", "B"]

# Test 3: Verifica que sem filhos, a chamada com first=True retorna lista vazia
def test__traversal_empty_children_returns_empty_with_first_true():
    root = DummyNode(value="root", children={})

    t = Trie()
    result = list(t._traversal(root, first=True))
    assert result == []
