import pytest
from repositorios.code_katas.src.string2num import string_to_number

# Test happy path: simple numeric string converts to int
def test_string_to_number_happy_path():
    assert string_to_number("123") == 123

# Test negative number string is parsed correctly
def test_string_to_number_negative():
    assert string_to_number("-45") == -45

# Test whitespace handling: leading spaces are ignored by int
def test_string_to_number_with_leading_spaces():
    assert string_to_number(" 7") == 7

# Test invalid numeric string raises ValueError
def test_string_to_number_invalid_raises_value_error():
    with pytest.raises(ValueError):
        string_to_number("abc")
