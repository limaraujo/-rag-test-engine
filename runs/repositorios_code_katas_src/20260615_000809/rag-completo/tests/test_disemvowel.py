from repositorios.code_katas.src.disemvowel import disemvowel

# happy path: removes vowels from a simple sentence with spaces
def test_happy_path_removes_vowels():
    assert disemvowel("hello world") == "hll wrld"

# edge case: both lowercase and uppercase vowels removed
def test_removes_all_present_vowels_case_mixed():
    assert disemvowel("AeIoU") == ""

# edge: no vowels present, string unchanged
def test_no_vowels_remain():
    assert disemvowel("bcdfg") == "bcdfg"

# punctuation and spaces preserved
def test_preserves_punctuation_and_spaces():
    assert disemvowel("hello, world!") == "hll, wrld!"
