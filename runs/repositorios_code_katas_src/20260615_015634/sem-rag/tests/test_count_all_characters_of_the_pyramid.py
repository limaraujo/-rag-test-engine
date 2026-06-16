from repositorios.code_katas.src.string_pyramid import count_all_characters_of_the_pyramid

# curto: happy path com entrada de tamanho 1
def test_count_all_characters_of_the_pyramid_single_character():
    assert count_all_characters_of_the_pyramid("a") == 1

# curto: happy path com entrada de tamanho 3
def test_count_all_characters_of_the_pyramid_three_characters():
    assert count_all_characters_of_the_pyramid("abc") == 35

# curto: borda com string vazia
def test_count_all_characters_of_the_pyramid_empty_string():
    assert count_all_characters_of_the_pyramid("") == -1

# curto: borda com None como entrada
def test_count_all_characters_of_the_pyramid_none_input():
    assert count_all_characters_of_the_pyramid(None) == -1
