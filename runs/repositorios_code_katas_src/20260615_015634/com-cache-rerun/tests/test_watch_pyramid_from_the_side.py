from repositorios.code_katas.src.string_pyramid import watch_pyramid_from_the_side

# curto
def test_watch_pyramid_from_the_side_abc_happy_path():
    # verifica caminho feliz com entrada 'abc'
    input_chars = "abc"
    expected = "  c  \n bbb \naaaaa"
    assert watch_pyramid_from_the_side(input_chars) == expected

# curto
def test_watch_pyramid_from_the_side_empty_string_edge_case():
    # verifica borda: entrada vazia retorna vazia
    assert watch_pyramid_from_the_side("") == ""

# curto
def test_watch_pyramid_from_the_side_single_character_borda():
    # verifica borda com apenas um caractere
    assert watch_pyramid_from_the_side("x") == "x"
