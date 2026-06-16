from repositorios.code_katas.src.trietree import Trie

class _DummyNode:
    def __init__(self):
        self.children = {}

# curto: happy path - verifica a inclusão do nó raiz e nós descendentes sem '$'
def test_traversal_happy_path_includes_root_and_descendants():
    t = Trie.__new__(Trie)
    root = _DummyNode()
    a = _DummyNode()
    b = _DummyNode()
    root.children['a'] = a
    a.children['b'] = b

    result = list(t._traversal(root))
    assert result == [root, a, b]

# curto: skip end-marker '$' durante travessia
def test_traversal_skips_dollar_end_markers():
    t = Trie.__new__(Trie)
    root = _DummyNode()
    a = _DummyNode()
    root.children['a'] = a
    root.children['$'] = _DummyNode()  # marcador de fim de palavra
    sub = _DummyNode()
    a.children['x'] = sub

    result = list(t._traversal(root))
    assert result == [root, a, sub]

# curto: não yields root quando first=True
def test_traversal_with_first_true_does_not_yield_root():
    t = Trie.__new__(Trie)
    root = _DummyNode()
    a = _DummyNode()
    root.children['a'] = a
    b = _DummyNode()
    a.children['b'] = b

    result = list(t._traversal(root, first=True))
    assert result == [a, b]

# curto: caminho com várias ramificações - verifica inclusão de nós de múltiplos ramos
def test_traversal_multiple_branches_includes_all_nodes():
    t = Trie.__new__(Trie)
    root = _DummyNode()
    a = _DummyNode()
    b = _DummyNode()
    c = _DummyNode()
    root.children['a'] = a
    root.children['b'] = b
    b.children['c'] = c

    result = list(t._traversal(root))
    assert result == [root, a, b, c]
