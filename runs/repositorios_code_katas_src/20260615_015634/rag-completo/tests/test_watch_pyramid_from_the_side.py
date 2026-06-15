from repositorios.code_katas.src.string_pyramid import watch_pyramid_from_the_side

# happy path: entrada 'ABC' gera a pirâmide esperada
def test_watch_pyramid_from_the_side_happy_path_three_chars():
    input_chars = "ABC"
    expected = "  C  \n BBB \nAAAAA"
    assert watch_pyramid_from_the_side(input_chars) == expected

# single character: entrada de um único caractere
def test_watch_pyramid_from_the_side_single_character():
    input_chars = "A"
    expected = "A"
    assert watch_pyramid_from_the_side(input_chars) == expected

# empty string: caso de borda com string vazia
def test_watch_pyramid_from_the_side_empty_string():
    input_chars = ""
    expected = ""
    assert watch_pyramid_from_the_side(input_chars) == expected

# None input: caso de borda com valor falsy
def test_watch_pyramid_from_the_side_none_input():
    input_chars = None
    expected = None
    assert watch_pyramid_from_the_side(input_chars) == expected
