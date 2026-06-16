import pytest
from repositorios.code_katas.src.trietree import Trie

# curto: happy path - palavra inserida é encontrada
def test_contains_happy_path_true():
    t = Trie()
    t.insert("cat")
    assert t.contains("cat") is True

# curto: caso de borda - prefixo existente mas não palavra completa levanta KeyError
def test_contains_prefix_raises_keyerror():
    t = Trie()
    t.insert("cat")
    with pytest.raises(KeyError):
        t.contains("ca")

# curto: caminho não existente resulta em False
def test_contains_nonexistent_path_returns_false():
    t = Trie()
    assert t.contains("dog") is False

# curto: tipo de argumento inválido levanta TypeError
def test_contains_wrong_type_raises_typeerror():
    t = Trie()
    with pytest.raises(TypeError):
        t.contains(123)
