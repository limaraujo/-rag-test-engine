import pytest
from repositorios.code_katas.src.string_pyramid import count_all_characters_of_the_pyramid

# verifica o branch: entradas falsy (vazia/None) retornam -1
@pytest.mark.parametrize("characters, expected", [
    ("", -1),
    (None, -1),
])
def test_falsy_inputs_parametrized(characters, expected):
    assert count_all_characters_of_the_pyramid(characters) == expected

# happy path: apenas um caractere
def test_single_character():
    assert count_all_characters_of_the_pyramid("A") == 1

# happy path: três caracteres
def test_three_characters():
    assert count_all_characters_of_the_pyramid("abc") == 35

# happy path: quatro caracteres
def test_four_characters():
    assert count_all_characters_of_the_pyramid("abcd") == 84
