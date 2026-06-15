import pytest
from repositorios.code_katas.src.string_pyramid import count_visible_characters_of_the_pyramid

# happy path: non-empty strings compute width^2 according to length
@pytest.mark.parametrize("characters,expected", [
    ("A", 1),
    ("AB", 9),
    ("ABC", 25),
    ("ABCDE", 81),
])
def test_count_visible_characters_of_the_pyramid_happy_path(characters, expected):
    assert count_visible_characters_of_the_pyramid(characters) == expected

# border cases: empty string or None should return -1
@pytest.mark.parametrize("characters,expected", [
    ("", -1),
    (None, -1),
])
def test_count_visible_characters_of_the_pyramid_edge_cases(characters, expected):
    assert count_visible_characters_of_the_pyramid(characters) == expected
