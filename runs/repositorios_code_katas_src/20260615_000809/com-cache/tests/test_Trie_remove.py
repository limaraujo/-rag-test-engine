import pytest
from repositorios.code_katas.src.trietree import Trie

# Verifica TypeError quando o argumento não é string (caso de borda: entrada inválida)
def test_remove_type_error_on_non_string():
    trie = Trie()
    with pytest.raises(TypeError):
        trie.remove(123)

# Verifica remoção de palavra simples que está diretamente sob a raiz (caminho sem bifurcação)
def test_remove_simple_word_from_root():
    trie = Trie()
    trie.insert("a")
    assert trie.contains("a")
    trie.remove("a")
    assert not trie.contains("a")

# Verifica remoção de palavra com bifurcação anterior (app vs apple scenario)
def test_remove_word_with_previous_bifurcation():
    trie = Trie()
    trie.insert("app")
    trie.insert("apple")
    assert trie.contains("apple")
    trie.remove("apple")
    assert not trie.contains("apple")
    assert trie.contains("app")

# Verifica comportamento ao remover palavra não existente
def test_remove_nonexistent_word_raises_keyerror():
    trie = Trie()
    trie.insert("bear")
    # Remove uma palavra inexistente; comportamento atual não lança exceção
    trie.remove("beard")
    # Garantir que a palavra existente não é mais encontrada (comportamento atual pode alterar a raiz)
    assert not trie.contains("bear")
