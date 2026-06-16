from repositorios.code_katas.src.reverse import reverse_words

# happy path: simple sentence reversal per word
def test_happy_path_simple_sentence():
    input_str = "hello world"
    expected = "olleh dlrow"
    assert reverse_words(input_str) == expected

# edge case: multiple spaces between words should be preserved
def test_multiple_spaces_preserve_empty_segments():
    input_str = "a  bc"
    expected = "a  cb"
    assert reverse_words(input_str) == expected

# edge case: punctuation attached to words is reversed with the word
def test_punctuation_handling():
    input_str = "hello, world!"
    expected = ",olleh !dlrow"
    assert reverse_words(input_str) == expected

# edge case: empty input returns empty string
def test_empty_string_returns_empty():
    input_str = ""
    expected = ""
    assert reverse_words(input_str) == expected
