import pytest
from repositorios.code_katas.src.string_pyramid import count_visible_characters_of_the_pyramid

# Test: happy path for non-empty inputs with varying lengths
@pytest.mark.parametrize("characters, expected", [
    ("A", 1),
    ("AB", 9),
    ("ABC", 25),
])
def test_count_visible_characters_non_empty_strings(characters, expected):
    assert count_visible_characters_of_the_pyramid(characters) == expected

# Test: branch where input is falsy (empty, None, or empty list) returns -1
@pytest.mark.parametrize("characters, expected", [
    ("", -1),
    (None, -1),
    ([], -1),
])
def test_count_visible_characters_falsy_inputs(characters, expected):
    assert count_visible_characters_of_the_pyramid(characters) == expected
