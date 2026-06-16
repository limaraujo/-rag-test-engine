from repositorios.code_katas.src.string_pyramid import count_visible_characters_of_the_pyramid

# happy path: non-empty string computes (2*len-1)^2
def test_count_visible_characters_of_the_pyramid_happy_path():
    assert count_visible_characters_of_the_pyramid("abc") == 25

# borda: empty string should return -1
def test_count_visible_characters_of_the_pyramid_empty_string():
    assert count_visible_characters_of_the_pyramid("") == -1

# borda: None should return -1
def test_count_visible_characters_of_the_pyramid_none():
    assert count_visible_characters_of_the_pyramid(None) == -1
