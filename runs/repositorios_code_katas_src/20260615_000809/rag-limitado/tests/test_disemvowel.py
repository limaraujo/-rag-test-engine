import pytest
from repositorios.code_katas.src.disemvowel import disemvowel

# happy path: remove vowels in normal strings (multiple scenarios)
@pytest.mark.parametrize("input_str, expected", [("hello world", "hll wrld"), ("Python", "Pythn")])
def test_disemvowel_happy_path(input_str, expected):
    assert disemvowel(input_str) == expected

# mixed-case and single-consonant: ensure uppercase vowels are removed and single consonant remains
def test_disemvowel_mixed_case_and_single_consonant():
    assert disemvowel("Aba") == "b"

# edge cases: empty string and strings without vowels should be preserved
@pytest.mark.parametrize("input_str, expected", [("", ""), ("h3ll0!", "h3ll0!")])
def test_disemvowel_edge_and_preserve(input_str, expected):
    assert disemvowel(input_str) == expected
