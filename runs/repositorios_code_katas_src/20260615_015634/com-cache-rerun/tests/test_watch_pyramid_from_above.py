from repositorios.code_katas.src.string_pyramid import watch_pyramid_from_above

# curto
def test_watch_pyramid_from_above_abc_happy_path():
    # verifica caminho feliz com entrada 'abc'
    input_chars = "abc"
    expected = "aaaaa\nabbba\nabcba\nabbba\naaaaa"
    assert watch_pyramid_from_above(input_chars) == expected

# curto
def test_watch_pyramid_from_above_empty_input():
    # verifica comportamento com string vazia (caso limite)
    input_chars = ""
    expected = ""
    assert watch_pyramid_from_above(input_chars) == expected

# curto
def test_watch_pyramid_from_above_single_character():
    # verifica caso de borda com apenas 1 caractere
    input_chars = "a"
    expected = "a"
    assert watch_pyramid_from_above(input_chars) == expected

# curto
def test_watch_pyramid_from_above_two_characters():
    # verifica caminho com entrada 'ab'
    input_chars = "ab"
    expected = "aaa\naba\naaa"
    assert watch_pyramid_from_above(input_chars) == expected
