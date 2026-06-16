from repositorios.code_katas.src.disemvowel import disemvowel

# happy path: remove vowels from a normal sentence
def test_disemvowel_happy_path_basic():
    input_str = "This is a test"
    expected = "Ths s  tst"
    assert disemvowel(input_str) == expected

# edge: empty string should remain empty
def test_disemvowel_empty_string():
    input_str = ""
    expected = ""
    assert disemvowel(input_str) == expected

# edge: string consisting only of vowels should become empty
def test_disemvowel_only_vowels():
    input_str = "aeiouAEIOU"
    expected = ""
    assert disemvowel(input_str) == expected

# edge: punctuation and spaces preserved, vowels removed
def test_disemvowel_preserve_punctuations_and_spaces():
    input_str = "Hello, world!"
    expected = "Hll, wrld!"
    assert disemvowel(input_str) == expected
