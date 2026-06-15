from repositorios.code_katas.src.reverse import reverse_words

# Verifica caminho feliz: duas palavras simples
def test_reverse_words_happy_path():
    s = "hello world"
    assert reverse_words(s) == "olleh dlrow"

# Verifica preservação de múltiplos espaços entre palavras
def test_reverse_words_preserves_multiple_spaces():
    s = "a  b"
    assert reverse_words(s) == "a  b"

# Verifica espaço no início da string é mantido
def test_reverse_words_leading_space():
    s = " hello"
    assert reverse_words(s) == " olleh"

# Verifica pontuação dentro de palavras é invertida adequadamente
def test_reverse_words_with_punctuation():
    s = "hi, there!"
    assert reverse_words(s) == ",ih !ereht"
