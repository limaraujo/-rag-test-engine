import pytest
from repositorios.code_katas.src.trietree import Trie

# caso feliz: palavra inserida é reconhecida
def test_contains_happy_path():
    t = Trie()
    t.insert("cat")
    assert t.contains("cat") is True

# ramo false: primeiro caractere ausente retorna False
def test_contains_unknown_root_char_returns_false():
    t = Trie()
    t.insert("cat")
    assert t.contains("z") is False

# exceção de tipo: não string levanta TypeError
def test_contains_type_error_for_non_string():
    t = Trie()
    with pytest.raises(TypeError):
        t.contains(123)

# exceção: prefixo de palavra inserida que não é palavra final levanta KeyError
def test_contains_prefix_not_included_raises_keyerror():
    t = Trie()
    t.insert("cat")
    with pytest.raises(KeyError) as exc:
        t.contains("ca")
    assert "That word has not been inserted" in str(exc.value)
