import pytest
from repositorios.code_katas.src.trietree import Trie

# verifica caminho feliz ao inserir uma palavra e garante que inserir novamente não aumenta o tamanho
def test_insert_basic_and_duplicate_increases_size_once():
    trie = Trie()
    trie.insert("hello")
    assert trie._size == 1
    trie.insert("hello")
    assert trie._size == 1

# verifica que inserção é case-insensitive e duplicatas não criam novos itens
def test_insert_case_insensitive_duplicate():
    trie = Trie()
    trie.insert("abc")
    trie.insert("ABC")
    assert trie._size == 1

# verifica que inserir com tipo não-string levanta TypeError
def test_insert_raises_type_error_for_non_string():
    trie = Trie()
    with pytest.raises(TypeError):
        trie.insert(123)

# verifica que inserir strings distintas aumenta o tamanho do trie
def test_insert_different_strings_increase_size():
    trie = Trie()
    trie.insert("cat")
    assert trie._size == 1
    trie.insert("dog")
    assert trie._size == 2
