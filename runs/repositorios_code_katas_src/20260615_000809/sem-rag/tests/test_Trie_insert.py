import pytest
from repositorios.code_katas.src.trietree import Trie

# Verifica TypeError ao passar não-string
def test_insert_raises_type_error_on_non_string():
    t = Trie()
    with pytest.raises(TypeError) as exc:
        t.insert(123)
    assert str(exc.value) == "Word must be a string"

# Verifica inserção de palavra nova aumenta o tamanho e marca fim com '$'
def test_insert_new_word_increases_size_and_sets_terminal():
    t = Trie()
    t.insert("Apple")
    assert t._size == 1
    cur = t.root
    for ch in "apple":
        assert ch in cur.children
        cur = cur.children[ch]
    assert '$' in cur.children
    assert cur.children['$'] == "apple"

# Verifica uso de prefixo existente entre palavras diferentes
def test_insert_with_existing_prefix_increases_size():
    t = Trie()
    t.insert("Apple")
    assert t._size == 1
    t.insert("App")
    assert t._size == 2
    cur = t.root
    for ch in "app":
        assert ch in cur.children
        cur = cur.children[ch]
    assert '$' in cur.children
    assert cur.children['$'] == "app"

# Verifica não incremento de tamanho ao reinserir a mesma palavra
def test_reinserting_same_word_does_not_increase_size():
    t = Trie()
    t.insert("Hello")
    cur = t.root
    for ch in "hello":
        cur = cur.children[ch]
    node = cur
    len_before = len(node.children)
    size_before = t._size
    t.insert("Hello")
    assert t._size == size_before
    assert len(node.children) == len_before
    assert node.children['$'] == "hello"
