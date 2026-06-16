import pytest
from repositorios.code_katas.src.reverse import reverse_words

# Test multiple scenarios for reverse_words: happy path, preserving multiple spaces, punctuation, and leading/trailing spaces
@pytest.mark.parametrize("input_str, expected", [
    ("hello world", "olleh dlrow"),
    ("a  b", "a  b"),
    ("Hello, World!", ",olleH !dlroW"),
    ("  hello  ", "  olleh  "),
])
def test_reverse_words_various_scenarios(input_str, expected):
    assert reverse_words(input_str) == expected
