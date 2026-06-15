from repositorios.code_katas.src.string_pyramid import count_visible_characters_of_the_pyramid

# curto: verifica caminho feliz com entrada não vazia
def test_count_visible_characters_of_the_pyramid_happy_path():
    chars = "ABC"
    expected = (2 * len(chars) - 1) ** 2
    assert count_visible_characters_of_the_pyramid(chars) == expected

# curto: verifica caso de borda com entrada vazia
def test_count_visible_characters_of_the_pyramid_empty_input():
    assert count_visible_characters_of_the_pyramid("") == -1
