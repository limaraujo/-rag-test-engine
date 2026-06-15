import pytest
from repositorios.code_katas.src.string_pyramid import count_visible_characters_of_the_pyramid

# Testa caminho feliz (varios comprimentos) da função.
@pytest.mark.parametrize("characters, expected", [
    ("a", 1),
    ("aa", 9),
    ("aaa", 25),
    ("aaaa", 49),
])
def test_count_visible_characters_of_the_pyramid_happy_path(characters, expected):
    assert count_visible_characters_of_the_pyramid(characters) == expected

# Testa caso de borda: entrada vazia ou None retorna -1
@pytest.mark.parametrize("characters", [None, ""])
def test_count_visible_characters_of_the_pyramid_empty_inputs(characters):
    assert count_visible_characters_of_the_pyramid(characters) == -1
