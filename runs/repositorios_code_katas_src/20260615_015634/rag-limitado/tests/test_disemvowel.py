import pytest
from repositorios.code_katas.src.disemvowel import disemvowel

# happy path: remove vowels from a typical sentence
def test_happy_path_basic():
    assert disemvowel("Hello World") == "Hll Wrld"

# edge case: string composed only of vowels -> empty string
def test_all_vowels_removed_inclusive_case():
    assert disemvowel("aeiouAEIOU") == ""

# edge case: string with no vowels -> unchanged
def test_no_vowels_present_remains_unchanged():
    assert disemvowel("BCDFGH") == "BCDFGH"

# mixed content: preserve non-vowel characters like spaces and punctuation
def test_mixed_punctuation_and_spaces_removed():
    assert disemvowel("This is a test!") == "Ths s  tst!"
