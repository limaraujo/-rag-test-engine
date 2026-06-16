import pytest
from repositorios.code_katas.src.string_pyramid import count_all_characters_of_the_pyramid

# curto: caminho principal - happy path
def test_count_all_characters_of_the_pyramid_happy_path():
    assert count_all_characters_of_the_pyramid("abc") == 35

# curto: casos com entradas falsy (caminho alternativo)
@pytest.mark.parametrize("characters", [None, "", [], False, 0])
def test_count_all_characters_of_the_pyramid_falsy_inputs(characters):
    assert count_all_characters_of_the_pyramid(characters) == -1
