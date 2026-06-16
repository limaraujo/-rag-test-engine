from repositorios.code_katas.src.reverse import reverse_words

# Verifica caminho feliz: duas palavras simples
def test_reverse_words_happy_path():
    s = "hello world"
    assert reverse_words(s) == "olleh dlrow"

# Verifica preservação de múltiplos espaços entre palavras
def test_reverse_words_multiple_spaces():
    s = "ab  cd"
    assert reverse_words(s) == "ba  dc"

# Verifica retorno para string vazia
def test_reverse_words_empty_string():
    s = ""
    assert reverse_words(s) == ""

# Verifica preservação de espaços no início
def test_reverse_words_leading_spaces():
    s = "  hello"
    assert reverse_words(s) == "  olleh"
