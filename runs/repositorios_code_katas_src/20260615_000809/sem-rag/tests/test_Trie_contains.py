import pytest
from repositorios.code_katas.src.trietree import Trie

# curto: happy path - palavra inserida com marcador terminal retorna True
def test_contains_happy_path():
    class Node:
        def __init__(self):
            self.children = {}

    t = Trie()
    t.root = Node()

    # build path 'cat'
    c = Node()
    t.root.children['c'] = c
    a = Node()
    c.children['a'] = a
    ta = Node()
    a.children['t'] = ta
    ta.children['$'] = True

    assert t.contains('cat') is True

# curto: missing_key - último nó não possui '$', espera KeyError
def test_contains_missing_key_raises_keyerror():
    class Node:
        def __init__(self):
            self.children = {}

    t = Trie()
    t.root = Node()

    d = Node()
    t.root.children['d'] = d
    o = Node()
    d.children['o'] = o
    # não adiciona '$' no nó final

    with pytest.raises(KeyError) as exc:
        t.contains('do')
    assert "That word has not been inserted" in str(exc.value)

# curto: branch onde o caminho parcial existe mas a próxima letra não está presente -> False
def test_contains_returns_false_when_path_not_found():
    class Node:
        def __init__(self):
            self.children = {}

    t = Trie()
    t.root = Node()

    c = Node()
    t.root.children['c'] = c
    a = Node()
    c.children['a'] = a
    # não adiciona 't' após 'ca', então tentativa de usar 'cb' ou similar falha no meio do caminho
    assert t.contains('cb') is False

# curto: tipo de entrada inválido lança TypeError
def test_contains_invalid_input_type_raises_typeerror():
    t = Trie()
    with pytest.raises(TypeError) as exc:
        t.contains(123)
    assert "Word must be a string" in str(exc.value)
