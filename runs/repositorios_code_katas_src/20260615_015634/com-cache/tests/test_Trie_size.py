import pytest
from repositorios.code_katas.src.trietree import Trie

# short: parametric test to verify that Trie.size reflects the number of unique words inserted,
# including cases with duplicates, across several sequences
@pytest.mark.parametrize("sequence, expected_size", [
    (["abc"], 1),
    (["abc", "abc"], 1),
    (["a", "ab", "abc", "abcd"], 4),
    (["hello", "world", "hello", "world"], 2),
    (["a", "aa", "aaa", "aa", "aaaa"], 4),
])
def test_size_counts_unique_words(sequence, expected_size):
    t = Trie()
    for s in sequence:
        t.insert(s)
    assert t.size() == expected_size
