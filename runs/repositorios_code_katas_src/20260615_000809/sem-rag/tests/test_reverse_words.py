from repositorios.code_katas.src.reverse import reverse_words

# Verifica caminho feliz: duas palavras simples invertidas
def test_happy_path():
    assert reverse_words("hello world") == "olleh dlrow"

# Verifica caso vazio devolve string vazia
def test_empty_string():
    assert reverse_words("") == ""

# Verifica preservação de múltiplos espaços entre palavras
def test_preserve_multiple_spaces():
    assert reverse_words("a  b") == "a  b"

# Verifica preservação de espaços no início e no fim da string
def test_leading_and_trailing_spaces_preserved():
    assert reverse_words("  hello ") == "  olleh "
