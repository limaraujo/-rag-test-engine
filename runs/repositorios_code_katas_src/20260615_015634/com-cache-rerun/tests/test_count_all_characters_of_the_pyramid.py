from repositorios.code_katas.src.string_pyramid import count_all_characters_of_the_pyramid

# happy path: three characters sum of (2n-1)^2 for n=3..1 equals 35
def test_count_all_characters_of_the_pyramid_happy_path_three_chars():
    assert count_all_characters_of_the_pyramid("abc") == 35

# edge/branch: empty string triggers the else branch and returns -1
def test_count_all_characters_of_the_pyramid_empty_returns_minus_one():
    assert count_all_characters_of_the_pyramid("") == -1
