import pytest
from repositorios.pyjwt.jwt.algorithms import Algorithm

# happy path: verify None is returned for a variety of input key values
@pytest.mark.parametrize("key", ["", "short", "this_is_a_key_of_sufficient_length_123", 12345, None])
def test_check_key_length_returns_none_for_various_inputs(key):
    assert Algorithm.check_key_length(None, key) is None

# edge case: unbound call should not raise and should return None
def test_check_key_length_unbound_call_does_not_raise():
    result = Algorithm.check_key_length(None, "any_key")
    assert result is None
