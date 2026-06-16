import pytest
from repositorios.code_katas.src.trietree import Trie

# Verifica caminho principal: inserir palavra nova, verificar terminal marker e lowercase
def test_insert_happy_path_lowercase_and_terminal_marker():
    trie = Trie()
    trie.insert("Hello")
    current = trie.root
    for ch in "hello":
        current = current.children[ch]
    assert '$' in current.children
    assert current.children['$'] == "hello"

# Verifica tratamento de tipo incorreto: lançar TypeError para entrada não-string
def test_insert_type_error_on_non_string():
    trie = Trie()
    with pytest.raises(TypeError):
        trie.insert(123)

# Verifica o branch quando há prefixo compartilhado entre palavras
def test_insert_with_shared_prefix_creates_branch_and_terminal_marker():
    trie = Trie()
    trie.insert("hello")
    trie.insert("help")
    current = trie.root
    for ch in "help":
        current = current.children[ch]
    assert '$' in current.children
    assert current.children['$'] == "help"

# Verifica comportamento ao inserir a mesma palavra novamente (sem duplicar terminal)
def test_insert_reinserting_same_word_no_duplicate_terminal():
    trie = Trie()
    trie.insert("hello")
    current = trie.root
    for ch in "hello":
        current = current.children[ch]
    assert '$' in current.children
    assert current.children['$'] == "hello"

    trie.insert("Hello")
    current2 = trie.root
    for ch in "hello":
        current2 = current2.children[ch]
    assert '$' in current2.children
    assert current2.children['$'] == "hello"
