import pytest
from repositorios.pyjwt.jwt.jwks_client import PyJWKClient


# helper dummy key object with a key_id attribute
class _DummyKey:
    def __init__(self, kid: str):
        self.key_id = kid

# short: happy path - a matching kid is found and returned
def test_match_kid_happy_path():
    signing_keys = [_DummyKey("a"), _DummyKey("b")]
    # Case: kid matches the second key
    result = PyJWKClient.match_kid(signing_keys, "b")
    assert result is signing_keys[1]

# short: edge case where kid does not exist in signing_keys
def test_match_kid_none_when_not_found():
    signing_keys = [_DummyKey("a"), _DummyKey("b")]
    # Case: kid not present should return None
    result = PyJWKClient.match_kid(signing_keys, "c")
    assert result is None

# short: ensure the first matching key is returned when multiple matches exist
def test_match_kid_returns_first_match():
    keys = [_DummyKey("dup"), _DummyKey("other"), _DummyKey("dup")]
    # Case: first occurrence should be returned
    result = PyJWKClient.match_kid(keys, "dup")
    assert result is keys[0]

# short: edge case with empty signing_keys list
def test_match_kid_empty_list():
    # Case: no keys to search should return None
    result = PyJWKClient.match_kid([], "anything")
    assert result is None
