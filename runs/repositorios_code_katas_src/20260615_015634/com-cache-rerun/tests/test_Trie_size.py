import pytest
from repositorios.code_katas.src.trietree import Trie

# curto: verifica que Trie.size retorna o número de palavras únicas após inserções,
# cobrindo caminho feliz, duplicatas, vazio e várias palavras distintas
@pytest.mark.parametrize("words, expected_size", [
    (["a", "ab", "abc"], 3),             # happy path: três palavras distintas
    (["a", "a", "aa", "aaa"], 3),        # duplicates não aumentam o tamanho
    ([], 0),                              # caso vazio
    (["cat", "car", "cart", "dog"], 4),   # várias palavras distintas em ramos diferentes
])
def test_size_counts_unique_words(words, expected_size):
    trie = Trie()
    for w in words:
        trie.insert(w)
    assert trie.size() == expected_size
