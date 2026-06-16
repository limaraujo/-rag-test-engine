from repositorios.code_katas.src.string_pyramid import watch_pyramid_from_above

# happy path: three-character input produces full pyramid
def test_watch_pyramid_from_above_three_chars():
    expected = "AAAAA\nABBBA\nABCBA\nABBBA\nAAAAA"
    assert watch_pyramid_from_above("ABC") == expected

# happy path: two-character input produces a smaller pyramid
def test_watch_pyramid_from_above_two_chars():
    expected = "AAA\nABA\nAAA"
    assert watch_pyramid_from_above("AB") == expected

# edge: empty input returns empty string
def test_watch_pyramid_from_above_empty_string():
    assert watch_pyramid_from_above("") == ""
