import pytest
from repositorios.code_katas.src.trietree import Trie

# Verifica caminho feliz: palavra inserida é encontrada
def test_contains_happy_path():
    trie = Trie()
    trie.insert("hello")
    assert trie.contains("hello") is True

# Verifica palavra não existente retorna False
def test_contains_nonexistent_path_returns_false():
    trie = Trie()
    trie.insert("hi")
    assert trie.contains("z") is False

# Verifica caso de borda em que o caminho existe, mas a palavra não foi inserida -> KeyError
def test_contains_prefix_without_end_marker_raises_keyerror():
    trie = Trie()
    trie.insert("cat")
    with pytest.raises(KeyError, match="That word has not been inserted"):
        trie.contains("ca")

# Verifica tipo de entrada incorreto levanta TypeError
def test_contains_non_string_raises_typeerror():
    trie = Trie()
    with pytest.raises(TypeError, match="Word must be a string"):
        trie.contains(123)
