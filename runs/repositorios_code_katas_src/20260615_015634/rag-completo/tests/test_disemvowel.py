import pytest
from repositorios.code_katas.src.disemvowel import disemvowel

# Test disemvowel removes vowels across multiple inputs (happy path and edge cases)
@pytest.mark.parametrize("input_str, expected", [
    ("Hello, World!", "Hll, Wrld!"),
    ("", ""),
    ("bcdfgh", "bcdfgh"),
    ("aeiouAEIOU", "")
])
def test_disemvowel_various_inputs(input_str, expected):
    assert disemvowel(input_str) == expected
