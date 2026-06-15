import pytest
from repositorios.code_katas.src.trietree import Trie

# happy path: inserir palavra simples e verificar contains
def test_insert_basic_and_contains():
    t = Trie()
    t.insert("cat")
    assert t.contains("cat") is True

# lowercasing: inserir com maiúsculas e verificar que é armazenado em minúsculas
def test_insert_lowercase_conversion():
    t = Trie()
    t.insert("Dog")
    assert t.contains("dog") is True

# branch: inserir palavras com o mesmo prefixo para exercitar criação de novas ramificações
# Branch: caminhos existentes e nova ramificação para um novo fim
def test_insert_branch_and_contains_both():
    t = Trie()
    t.insert("cat")
    t.insert("car")
    assert t.contains("cat") is True
    assert t.contains("car") is True

# exception: passagem de tipo não-string levanta TypeError
def test_insert_type_error():
    t = Trie()
    with pytest.raises(TypeError):
        t.insert(123)
