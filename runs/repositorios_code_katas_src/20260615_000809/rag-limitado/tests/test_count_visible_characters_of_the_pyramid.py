from repositorios.code_katas.src.string_pyramid import count_visible_characters_of_the_pyramid

# verifica caminho principal com entrada não vazia
def test_count_visible_characters_of_the_pyramid_happy_path():
    input_chars = "ABC"
    expected = 25  # (2*len("ABC") - 1)^2 = (5)^2 = 25
    assert count_visible_characters_of_the_pyramid(input_chars) == expected

# verifica o caso em que a entrada é None (branch falsy)
def test_count_visible_characters_of_the_pyramid_none_returns_minus_one():
    assert count_visible_characters_of_the_pyramid(None) == -1

# verifica o caso em que a entrada é string vazia (branch falsy)
def test_count_visible_characters_of_the_pyramid_empty_string_returns_minus_one():
    assert count_visible_characters_of_the_pyramid("") == -1
