import pytest
from repositorios.pyjwt.jwt.api_jwt import PyJWT

class _TestPyJWT(PyJWT):
    def __init__(self, options):
        # bypass base __init__ to set options directly
        self.options = options

# happy path: both options provided with explicit boolean values
@pytest.mark.parametrize("options, expected", [
    ({"verify_signature": True, "enforce_minimum_key_length": True},
     {"verify_signature": True, "enforce_minimum_key_length": True}),
    ({"verify_signature": False, "enforce_minimum_key_length": False},
     {"verify_signature": False, "enforce_minimum_key_length": False}),
])
def test_get_sig_options_happy_path_various(options, expected):
    obj = _TestPyJWT(options)
    assert obj._get_sig_options() == expected

# default enforce_minimum_key_length -> False when not provided
def test_get_sig_options_default_enforce_missing():
    obj = _TestPyJWT({"verify_signature": True})
    assert obj._get_sig_options() == {
        "verify_signature": True,
        "enforce_minimum_key_length": False,
    }

# missing verify_signature should raise a KeyError
def test_get_sig_options_missing_verify_signature_raises():
    obj = _TestPyJWT({"enforce_minimum_key_length": True})
    with pytest.raises(KeyError):
        obj._get_sig_options()
