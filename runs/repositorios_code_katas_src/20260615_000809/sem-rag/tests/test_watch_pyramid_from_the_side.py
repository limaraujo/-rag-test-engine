from repositorios.code_katas.src.string_pyramid import watch_pyramid_from_the_side

# Teste principal (happy path) com várias letras
def test_watch_pyramid_from_the_side_happy_path_multiple_chars():
    expected = "  C  \n BBB \nAAAAA"
    assert watch_pyramid_from_the_side("ABC") == expected

# Teste com único caractere (caminho simples)
def test_watch_pyramid_from_the_side_single_char():
    expected = "A"
    assert watch_pyramid_from_the_side("A") == expected

# Teste com entrada vazia (caso limite)
def test_watch_pyramid_from_the_side_empty_string():
    expected = ""
    assert watch_pyramid_from_the_side("") == expected
