import pytest
from repositorios.code_katas.src.alt_case import to_alternating_case

# happy path: standard string with letters, space and punctuation
def test_to_alternating_case_happy_path():
    assert to_alternating_case("Hello World!") == "hELLO wORLD!"

# edge case: empty string should return empty string
def test_to_alternating_case_empty_string():
    assert to_alternating_case("") == ""

# mixed characters: digits remain unchanged, letters swap case
def test_to_alternating_case_mixed_characters():
    assert to_alternating_case("123abc") == "123ABC"

# exception path: non-string input should raise TypeError
def test_to_alternating_case_non_string_raises_type_error():
    with pytest.raises(TypeError):
        to_alternating_case(None)
