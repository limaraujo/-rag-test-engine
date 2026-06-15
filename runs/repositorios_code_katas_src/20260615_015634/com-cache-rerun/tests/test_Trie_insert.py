import pytest
from repositorios.code_katas.src.trietree import Trie

# Verifica TypeError ao tentar inserir valor não-string
def test_insert_raises_type_error_on_non_string():
    t = Trie()
    with pytest.raises(TypeError):
        t.insert(123)

# Verifica happy path: inserir palavra cria caminho de nós, marca fim com '$' e aumenta tamanho
def test_insert_happy_path_creates_path_and_marks_end():
    t = Trie()
    t.insert("apple")
    assert t.contains("apple") is True
    assert t._size == 1

# Verifica que inserir palavra existente não aumenta o tamanho (_size)
def test_insert_duplicate_increases_size_only_once():
    t = Trie()
    t.insert("banana")
    t.insert("banana")
    assert t._size == 1
    assert t.contains("banana") is True

# Verifica inserção de string vazia: registra fim na raiz e aumenta tamanho
def test_insert_empty_string_marks_end_and_size():
    t = Trie()
    t.insert("")
    assert t._size == 1
    assert '$' in t.root.children
    assert t.root.children['$'] == ""
