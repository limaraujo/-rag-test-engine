import pytest
from repositorios.code_katas.src.trietree import Trie

# Verifica o tamanho inicial é 0 antes de inserir qualquer palavra (caso happy path)
def test_size_initial_zero():
    t = Trie()
    assert t.size() == 0

# Verifica que tamanho aumenta com inserções de palavras distintas e não aumenta com duplicatas
def test_size_increases_and_no_duplicates():
    t = Trie()
    t.insert("cat")
    t.insert("car")
    t.insert("dog")
    assert t.size() == 3
    t.insert("cat")  # duplicata não deve incrementar o tamanho
    assert t.size() == 3

# Verifica tamanho com palavras que compartilham prefixos e duplicatas não aumentam o tamanho
def test_size_with_shared_prefixes_and_duplicates():
    t = Trie()
    t.insert("to")
    t.insert("tea")
    t.insert("ted")
    assert t.size() == 3
    t.insert("tea")  # duplicata
    assert t.size() == 3
