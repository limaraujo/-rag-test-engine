import pytest
from repositorios.code_katas.src.trietree import Trie

# curto: verifica path feliz ao inserir uma nova palavra na trie vazia
def test_insert_happy_path_increases_size_and_stores_word():
    trie = Trie()
    assert trie._size == 0
    trie.insert("Hello")
    assert trie._size == 1

    current = trie.root
    for ch in "hello":
        assert ch in current.children
        current = current.children[ch]
    assert '$' in current.children
    assert current.children['$'] == "hello"

# curto: verifica que inserir a mesma palavra não aumenta o tamanho
def test_insert_duplicate_word_does_not_increase_size():
    trie = Trie()
    trie.insert("Hello")
    assert trie._size == 1

    trie.insert("Hello")
    assert trie._size == 1  # não deve aumentar ao inserir palavra existente

    current = trie.root
    for ch in "hello":
        assert ch in current.children
        current = current.children[ch]
    assert '$' in current.children
    assert current.children['$'] == "hello"

# curto: verifica exceção quando o input não é string
def test_insert_non_string_raises_type_error():
    trie = Trie()
    with pytest.raises(TypeError) as excinfo:
        trie.insert(123)
    assert "Word must be a string" in str(excinfo.value)

# curto: verifica que o input é convertido para minúsculas antes de inserir
def test_insert_lowercases_input_and_creates_lowercased_path():
    trie = Trie()
    trie.insert("ApPlE")
    assert trie._size == 1

    current = trie.root
    for ch in "apple":
        assert ch in current.children
        current = current.children[ch]
    assert '$' in current.children
    assert current.children['$'] == "apple"
