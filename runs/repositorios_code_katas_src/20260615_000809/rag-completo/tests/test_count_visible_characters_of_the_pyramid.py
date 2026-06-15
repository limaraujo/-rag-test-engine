import pytest
from repositorios.code_katas.src.string_pyramid import count_visible_characters_of_the_pyramid

# Teste: caminho principal - entradas não vazias (happy path) com diferentes comprimentos
@pytest.mark.parametrize("characters, expected", [
    ("A", 1),
    ("AB", 9),
    ("ABC", 25),
])
def test_count_visible_characters_of_the_pyramid_happy_path(characters, expected):
    assert count_visible_characters_of_the_pyramid(characters) == expected

# Teste: borda - string vazia deve retornar -1
def test_count_visible_characters_of_the_pyramid_empty_string():
    assert count_visible_characters_of_the_pyramid("") == -1

# Teste: borda - None deve retornar -1
def test_count_visible_characters_of_the_pyramid_none():
    assert count_visible_characters_of_the_pyramid(None) == -1
