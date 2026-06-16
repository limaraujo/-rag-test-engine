from repositorios.code_katas.src.string_pyramid import watch_pyramid_from_the_side

# happy path: pyramid generated from the string "ABC"
def test_watch_pyramid_from_side_abc():
    assert watch_pyramid_from_the_side("ABC") == "  C  \n BBB \nAAAAA"

# edge case: empty input should return empty string
def test_watch_pyramid_from_side_empty():
    assert watch_pyramid_from_the_side("") == ""

# minimal non-empty input: single character should return that character
def test_watch_pyramid_from_side_single_char():
    assert watch_pyramid_from_the_side("A") == "A"
