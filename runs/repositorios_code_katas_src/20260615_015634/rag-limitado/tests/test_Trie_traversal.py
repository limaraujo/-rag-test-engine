from types import MethodType
from repositorios.code_katas.src.trietree import Trie

# Testa caminho sem start (happy path) — usa _traversal para gerar palavras
def test_traversal_no_start_yields_values():
    t = Trie()
    class DummyRoot:
        def __init__(self):
            self.children = {}
    t.root = DummyRoot()

    class WordObj:
        def __init__(self, v):
            self.value = v

    def fake_traversal(self, node, first):
        yield WordObj("apple")
        yield WordObj("application")

    t._traversal = MethodType(fake_traversal, t)
    assert list(t.traversal()) == ["apple", "application"]

# Testa caminho com prefixo existente — verifica saída ordenada de palavras sob o prefixo
def test_traversal_with_existing_prefix_yields_values():
    t = Trie()
    class DummyRoot:
        def __init__(self):
            self.children = {'a': object()}
    t.root = DummyRoot()

    class WordObj:
        def __init__(self, v):
            self.value = v

    def fake_traversal(self, node, first):
        yield WordObj("ant")
        yield WordObj("anteater")

    t._traversal = MethodType(fake_traversal, t)
    assert list(t.traversal("a")) == ["ant", "anteater"]

# Testa prefixo ausente — não deve ocorrer _traversal e gerar lista vazia
def test_traversal_missing_prefix_yields_none():
    t = Trie()
    class DummyRoot:
        def __init__(self):
            self.children = {}
    t.root = DummyRoot()

    def fail_traversal(self, node, first):
        raise AssertionError("A _traversal não deve ser chamada quando o prefixo não existe")

    t._traversal = MethodType(fail_traversal, t)
    assert list(t.traversal("z")) == []

# Testa prefixo vazio (start="") — é tratado como ausência de start
def test_traversal_empty_prefix_ignored_yields_values():
    t = Trie()
    class DummyRoot:
        def __init__(self):
            self.children = {'b': object()}
    t.root = DummyRoot()

    class WordObj:
        def __init__(self, v):
            self.value = v

    def fake_traversal(self, node, first):
        yield WordObj("bat")

    t._traversal = MethodType(fake_traversal, t)
    assert list(t.traversal("")) == ["bat"]
