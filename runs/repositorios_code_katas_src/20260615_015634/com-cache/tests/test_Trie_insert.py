import pytest
from repositorios.code_katas.src.trietree import Trie

# Teste de exceção: inserting não-string deve raise TypeError
def test_insert_raises_type_error_on_non_string():
    t = Trie()
    with pytest.raises(TypeError):
        t.insert(123)

# Teste feliz: inserção cria nós internos e marcador de fim com string em lowercase
def test_insert_creates_internal_nodes_and_terminal_marker():
    t = Trie()
    t.insert("Cat")
    current = t.root
    for ch in "cat":
        assert ch in current.children
        current = current.children[ch]
    assert '$' in current.children
    assert current.children['$'] == "cat"

# Teste de múltiplas strings com prefixo compartilhado: verifica caminhos diferentes
def test_insert_multiple_strings_with_shared_prefix():
    t = Trie()
    t.insert("cat")
    t.insert("car")
    # Verifica caminho para "cat"
    current = t.root
    for ch in "ca":
        assert ch in current.children
        current = current.children[ch]
    assert 't' in current.children
    current = current.children['t']
    assert '$' in current.children
    assert current.children['$'] == "cat"
    # Verifica caminho para "car"
    current = t.root
    for ch in "car":
        assert ch in current.children
        current = current.children[ch]
    assert '$' in current.children
    assert current.children['$'] == "car"

# Teste de borda: inserir string vazia
def test_insert_empty_string_results_in_root_marker():
    t = Trie()
    t.insert("")
    assert '$' in t.root.children
    assert t.root.children['$'] == ""
