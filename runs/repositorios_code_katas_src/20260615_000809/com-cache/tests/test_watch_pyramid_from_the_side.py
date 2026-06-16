from repositorios.code_katas.src.string_pyramid import watch_pyramid_from_the_side

# Verifica caminho feliz com uma única letra (caso simples)
def test_happy_path_single_character():
    assert watch_pyramid_from_the_side("A") == "A"

# Verifica caminho feliz com várias letras formando pyramid
def test_happy_path_multiple_characters():
    input_str = "ABC"
    expected = "  C  \n BBB \nAAAAA"
    assert watch_pyramid_from_the_side(input_str) == expected

# Verifica branch quando input é None
def test_none_input_returns_none():
    assert watch_pyramid_from_the_side(None) is None

# Verifica caso de borda: string vazia
def test_empty_string_returns_empty():
    assert watch_pyramid_from_the_side("") == ""
