import pytest
from repositorios.code_katas.src.trietree import Trie

# Verifica inserção de duas palavras com caminho compartilhado e verificação de tamanho
def test_insert_happy_path_multiple_words_and_size():
    t = Trie()
    t.insert("cat")
    t.insert("car")
    assert t.contains("cat") is True
    assert t.contains("car") is True
    assert t._size == 2

# Verifica que inserção duplicada não aumenta o tamanho
def test_insert_duplicate_does_not_increase_size():
    t = Trie()
    t.insert("dog")
    t.insert("dog")
    assert t.contains("dog") is True
    assert t._size == 1

# Verifica normalização para minúsculas
def test_insert_lowercase_normalization():
    t = Trie()
    t.insert("Bird")
    assert t.contains("bird") is True
    assert t._size == 1

# Verifica exceção para tipo não-string
def test_insert_invalid_type_raises_type_error():
    t = Trie()
    with pytest.raises(TypeError, match="Word must be a string"):
        t.insert(123)
