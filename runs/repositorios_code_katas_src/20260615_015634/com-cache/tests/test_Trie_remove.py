import pytest
from repositorios.code_katas.src.trietree import Trie

# Verifica TypeError quando o input não é string
def test_remove_non_string_raises_type_error():
    t = Trie()
    with pytest.raises(TypeError):
        t.remove(123)

# Verifica KeyError quando a palavra não está presente no trie
def test_remove_word_not_in_trie_raises_keyerror():
    t = Trie()
    t.insert("apple")
    with pytest.raises(KeyError):
        t.remove("banana")

# Verifica remoção de palavra com caminho simples (sem bifurcação)
def test_remove_word_without_shared_prefix_happy_path():
    t = Trie()
    t.insert("cat")
    t.remove("cat")
    assert not t.contains("cat")

# Verifica remoção de palavra com prefixo compartilhado preservando outra palavra
def test_remove_word_with_shared_prefix_preserves_other():
    t = Trie()
    t.insert("cat")
    t.insert("car")
    assert t.contains("cat") and t.contains("car")
    t.remove("cat")
    assert not t.contains("cat")
    assert t.contains("car")
