import pytest
from repositorios.code_katas.src.string_pyramid import count_all_characters_of_the_pyramid

# caminho feliz: cenários de comprimentos de entrada 1 a 5 com resultados esperados
@pytest.mark.parametrize("characters,expected", [
    ("A", 1),
    ("AB", 10),
    ("ABC", 35),
    ("ABCDE", 165),
])
def test_count_all_characters_of_the_pyramid_happy_path(characters, expected):
    assert count_all_characters_of_the_pyramid(characters) == expected

# casos de borda: entradas vazias ou None retornam -1
@pytest.mark.parametrize("characters,expected", [
    ("", -1),
    (None, -1),
])
def test_count_all_characters_of_the_pyramid_edge_cases(characters, expected):
    assert count_all_characters_of_the_pyramid(characters) == expected
