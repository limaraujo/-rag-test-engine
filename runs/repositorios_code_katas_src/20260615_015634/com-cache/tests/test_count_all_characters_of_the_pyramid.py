from repositorios.code_katas.src.string_pyramid import count_all_characters_of_the_pyramid

# happy path: string with 3 characters -> sum of (2n-1)^2 for n=3..1 equals 35
def test_count_all_characters_of_the_pyramid_happy_path_three_chars():
    assert count_all_characters_of_the_pyramid("abc") == 35

# basic path: single character -> (2*1-1)^2 = 1
def test_count_all_characters_of_the_pyramid_single_character():
    assert count_all_characters_of_the_pyramid("a") == 1

# edge case: empty input should return -1
def test_count_all_characters_of_the_pyramid_empty_string_returns_minus_one():
    assert count_all_characters_of_the_pyramid("") == -1

# longer input: 4 characters -> 7^2 + 5^2 + 3^2 + 1^2 = 84
def test_count_all_characters_of_the_pyramid_four_chars_happy_path():
    assert count_all_characters_of_the_pyramid("abcd") == 84
