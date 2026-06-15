from repositorios.code_katas.src.string_pyramid import watch_pyramid_from_above

# verifica caminho feliz com entrada 'abc'
def test_watch_pyramid_from_above_abc():
    input_chars = "abc"
    expected = "aaaaa\nabbba\nabcba\nabbba\naaaaa"
    assert watch_pyramid_from_above(input_chars) == expected

# verifica caso de borda com entrada vazia
def test_watch_pyramid_from_above_empty_string():
    input_chars = ""
    expected = ""
    assert watch_pyramid_from_above(input_chars) == expected

# verifica caso de borda com único caractere
def test_watch_pyramid_from_above_single_character():
    input_chars = "a"
    expected = "a"
    assert watch_pyramid_from_above(input_chars) == expected
