import pytest
from repositorios.code_katas.src.trietree import Trie

# Verifica tamanho inicial é zero ao criar a Trie (happy path)
def test_size_initially_zero():
    t = Trie()
    assert t.size() == 0

# Verifica: tamanho aumenta com insert(s) de palavras distintas (happy path)
def test_size_increases_with_distinct_insertions():
    t = Trie()
    t.insert("cat")
    t.insert("car")
    t.insert("dog")
    assert t.size() == 3

# Verifica: duplicatas não aumentam o tamanho (edge case)
def test_size_does_not_increment_on_duplicate_insertions():
    t = Trie()
    t.insert("apple")
    assert t.size() == 1
    t.insert("apple")
    assert t.size() == 1

# Cobertura parametrizada: cenários com palavras distintas, duplicadas e mistura
@pytest.mark.parametrize("words,expected", [
    (["cat", "car", "dog"], 3),
    (["apple", "apple", "banana", "banana", "cherry"], 3),
    (["test", "team", "teaser", "test"], 3),
])
def test_size_handles_multiple_words_and_duplicates(words, expected):
    t = Trie()
    for w in words:
        t.insert(w)
    assert t.size() == expected
