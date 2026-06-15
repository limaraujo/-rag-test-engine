from repositorios.code_katas.src.string_pyramid import count_visible_characters_of_the_pyramid

# happy path: 3 characters -> width 5 -> 25
def test_count_visible_characters_of_the_pyramid_happy_path_three_chars():
    assert count_visible_characters_of_the_pyramid("abc") == 25

# happy path: 1 character -> width 1 -> 1
def test_count_visible_characters_of_the_pyramid_happy_path_single_char():
    assert count_visible_characters_of_the_pyramid("a") == 1

# edge case: empty string -> -1
def test_count_visible_characters_of_the_pyramid_empty_string():
    assert count_visible_characters_of_the_pyramid("") == -1

# edge case: None input -> -1
def test_count_visible_characters_of_the_pyramid_none_input():
    assert count_visible_characters_of_the_pyramid(None) == -1
