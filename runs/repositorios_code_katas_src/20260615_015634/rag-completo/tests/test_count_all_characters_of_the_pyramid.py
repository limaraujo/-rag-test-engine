import pytest
from repositorios.code_katas.src.string_pyramid import count_all_characters_of_the_pyramid


# happy path: verifica soma para comprimentos 1, 2 e 3
@pytest.mark.parametrize("characters, expected", [
    ("a", 1),
    ("ab", 10),
    ("abc", 35),
])
def test_count_all_characters_of_the_pyramid_happy_path(characters, expected):
    assert count_all_characters_of_the_pyramid(characters) == expected

# borda: entrada vazia retorna -1
def test_count_all_characters_of_the_pyramid_empty_input_returns_minus_one():
    assert count_all_characters_of_the_pyramid("") == -1
