import pytest
from repositorios.code_katas.src.trietree import Trie


# Verifica caminho existente (start='ab') e retorno de valores pela traversal com _traversal mocked
def test_traversal_existing_path_yields_values(monkeypatch):
    class Val:
        def __init__(self, v):
            self.value = v

    vals = [Val('apple'), Val('banana')]

    def fake_trav(self, current, flag):
        return vals

    monkeypatch.setattr(Trie, "_traversal", fake_trav, raising=True)

    t = object.__new__(Trie)
    class Node:
        def __init__(self):
            self.children = {}
    root = Node()
    root.children['a'] = Node()
    root.children['a'].children['b'] = Node()
    t.root = root

    result = list(t.traversal('ab'))
    assert result == ['apple', 'banana']


# Verifica funcionamento quando start não é fornecido (happy path)
def test_traversal_no_start_yields_values(monkeypatch):
    class Val:
        def __init__(self, v):
            self.value = v

    vals = [Val('dog'), Val('cat')]

    def fake_trav(self, current, flag):
        return vals

    monkeypatch.setattr(Trie, "_traversal", fake_trav, raising=True)

    t = object.__new__(Trie)
    t.root = object()

    result = list(t.traversal())
    assert result == ['dog', 'cat']


# Verifica caminho ausente (start leva a missing letter) não produz saída
def test_traversal_missing_path_yields_none(monkeypatch):
    t = object.__new__(Trie)

    class Node:
        def __init__(self):
            self.children = {}

    root = Node()
    root.children['a'] = Node()
    # 'a' doesn't have 'c' in its children, path should be missing
    t.root = root

    def should_not_call(self, current, flag):
        raise AssertionError("traversal should not call _traversal when path is missing")

    monkeypatch.setattr(Trie, "_traversal", should_not_call, raising=True)

    result = list(t.traversal('ac'))
    assert result == []


# Verifica caminho existente, mas _traversal retorna vazio
def test_traversal_existing_path_empty_results(monkeypatch):
    class Val:
        def __init__(self, v):
            self.value = v

    def fake_trav(self, current, flag):
        return []

    monkeypatch.setattr(Trie, "_traversal", fake_trav, raising=True)

    t = object.__new__(Trie)
    class Node:
        def __init__(self):
            self.children = {}
    root = Node()
    root.children['a'] = Node()
    root.children['a'].children['b'] = Node()
    t.root = root

    result = list(t.traversal('ab'))
    assert result == []
