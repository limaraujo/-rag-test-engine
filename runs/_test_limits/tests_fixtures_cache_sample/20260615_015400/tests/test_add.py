from tests.fixtures.cache_sample.add import add

def test_add_ok():
    assert add(1, 2) == 3
