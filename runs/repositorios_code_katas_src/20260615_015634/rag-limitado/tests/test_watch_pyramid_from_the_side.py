from repositorios.code_katas.src.string_pyramid import watch_pyramid_from_the_side


# test: happy path with multiple characters -> proper pyramid side view
def test_watch_pyramid_side_happy_path_abc():
    # happy path: input "abc" produces a three-line pyramid from the side
    assert watch_pyramid_from_the_side("abc") == "  c  \n bbb \naaaaa"


# test: single character input -> single line with that character
def test_watch_pyramid_side_single_char():
    # edge case: single character should return that character as a single line
    assert watch_pyramid_from_the_side("x") == "x"


# test: empty string input -> returns empty string (falsy branch)
def test_watch_pyramid_side_empty_string():
    # edge case: empty input should return empty string
    assert watch_pyramid_from_the_side("") == ""


# test: None input -> returns None (falsy branch)
def test_watch_pyramid_side_none_input():
    # edge case: None input should return None
    assert watch_pyramid_from_the_side(None) is None
