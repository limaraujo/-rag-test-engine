from repositorios.code_katas.src.reverse import reverse_words

# verifica caminho feliz: várias palavras simples
def test_reverse_words_happy_path():
    input_str = "The quick brown fox"
    expected = "ehT kciuq nworb xof"
    assert reverse_words(input_str) == expected

# verifica preservação de espaços múltiplos
def test_reverse_words_preserve_multiple_spaces():
    input_str = "a  b"
    expected = "a  b"
    assert reverse_words(input_str) == expected

# verifica caso vazio
def test_reverse_words_empty_string():
    input_str = ""
    expected = ""
    assert reverse_words(input_str) == expected

# verifica pontuação é invertida por palavra mantendo separadores
def test_reverse_words_with_punctuation():
    input_str = "Hello, world!"
    expected = ",olleH !dlrow"
    assert reverse_words(input_str) == expected
