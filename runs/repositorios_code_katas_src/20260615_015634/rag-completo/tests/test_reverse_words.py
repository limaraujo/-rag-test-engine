import pytest
from repositorios.code_katas.src.reverse import reverse_words

# Verifica múltiplos cenários com entradas variadas (caminho feliz e bordas)
@pytest.mark.parametrize("inp, expected", [
    ("hello world", "olleh dlrow"),    # happy path: duas palavras
    ("a  b", "a  b"),                   # preserva múltiplos espaços
    ("  hello", "  olleh"),             # preserva espaços no início
    ("", ""),                            # entrada vazia
    ("hi!", "!ih"),                       # pontuação dentro da palavra
    ("abc def!", "cba !fed"),            # pontuação no final da segunda palavra
])
def test_reverse_words_various_cases(inp, expected):
    assert reverse_words(inp) == expected
