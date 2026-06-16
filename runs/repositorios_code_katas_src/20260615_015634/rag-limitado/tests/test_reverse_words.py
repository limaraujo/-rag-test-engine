import pytest
from repositorios.code_katas.src.reverse import reverse_words

# happy path: várias entradas comuns, confirmando a reversão de cada palavra
@pytest.mark.parametrize("inp, expected", [
    ("hello world", "olleh dlrow"),
    ("reverse_words", "sdrow_esrever"),
    ("1234 56", "4321 65"),
    ("a b c", "a b c"),
])
def test_reverse_words_happy_path_param(inp, expected):
    assert reverse_words(inp) == expected

# borda: espaços, string vazia e múltiplos espaços entre palavras
def test_reverse_words_space_and_edgecases():
    assert reverse_words(" a") == " a"
    assert reverse_words("a ") == "a "
    assert reverse_words("") == ""
    assert reverse_words("a  b") == "a  b"

# exceção: entrada não-string deve levantar AttributeError ao usar .split
def test_reverse_words_invalid_input_raises():
    with pytest.raises(AttributeError):
        reverse_words(1)
