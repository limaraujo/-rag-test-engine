import pytest
from repositorios.code_katas.src.trietree import Trie

# Casos de borda: trie vazia deve retornar tamanho 0
def test_size_initially_zero():
    t = Trie()
    assert t.size() == 0

# Caminho feliz: várias palavras inseridas; duplicatas não contam como palavras adicionais
@pytest.mark.parametrize("words, expected", [
    (["cat","car","cart"], 3),
    (["apple","apple","banana"], 2),
])
def test_size_counts_unique_words(words, expected):
    t = Trie()
    for w in words:
        t.insert(w)
    assert t.size() == expected
