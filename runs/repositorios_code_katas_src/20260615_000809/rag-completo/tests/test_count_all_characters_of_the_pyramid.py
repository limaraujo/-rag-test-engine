from repositorios.code_katas.src.string_pyramid import count_all_characters_of_the_pyramid

# happy path: length 3 (abc) produces sum of odd squares: 25 + 9 + 1 = 35
def test_count_all_characters_of_the_pyramid_happy_path_three_chars():
    assert count_all_characters_of_the_pyramid("abc") == 35

# edge: empty string should return -1 (branch where characters is falsy)
# edge: empty input
def test_count_all_characters_of_the_pyramid_empty_string_returns_minus_one():
    assert count_all_characters_of_the_pyramid("") == -1

# edge: single character should return 1
# single character
def test_count_all_characters_of_the_pyramid_single_character():
    assert count_all_characters_of_the_pyramid("a") == 1

# edge: None should return -1 (falsy input path)
# none input
def test_count_all_characters_of_the_pyramid_none_returns_minus_one():
    assert count_all_characters_of_the_pyramid(None) == -1
