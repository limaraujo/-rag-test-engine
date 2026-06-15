import pytest
from repositorios.code_katas.src.reverse import reverse_words


# Verifica reversão de palavras em casos normais (caminho feliz e borda)
@pytest.mark.parametrize("input_str, expected", [
    ("hello world", "olleh dlrow"),
    ("Hello", "olleH"),
    ("a  b", "a  b"),
    ("", "")
])
def test_reverse_words_normal_cases(input_str, expected):
    assert reverse_words(input_str) == expected

# Verifica exceção ao receber input não-string (comportamento esperado)
def test_reverse_words_raises_on_non_string_input():
    with pytest.raises(AttributeError):
        reverse_words(123)
