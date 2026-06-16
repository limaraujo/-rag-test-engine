import pytest
from repositorios.code_katas.src.trietree import Trie

# happy path: tamanho reflete palavras únicas e não aumenta com duplicatas
def test_size_increments_with_unique_words_and_ignores_duplicates():
    trie = Trie()
    assert trie.size() == 0
    trie.insert("cat")
    assert trie.size() == 1
    trie.insert("dog")
    assert trie.size() == 2
    trie.insert("cat")  # duplicate
    assert trie.size() == 2

# caminho com palavras com prefixos: cada inserção de palavra distinta aumenta size
def test_size_with_prefix_words_increases_per_unique_word():
    trie = Trie()
    for word in ["a", "ab", "abc", "abcd"]:
        trie.insert(word)
    assert trie.size() == 4
    trie.insert("ab")  # duplicata
    assert trie.size() == 4

# idempotente com repetição de mesma palavra
def test_size_idempotent_with_duplicate_inserts():
    trie = Trie()
    trie.insert("x")
    for _ in range(5):
        trie.insert("x")
    assert trie.size() == 1
