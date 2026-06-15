from repositorios.pyjwt.jwt.api_jwt import PyJWT

def _make_pyjwt(opts):
    obj = PyJWT.__new__(PyJWT)
    obj.options = opts
    return obj

# curto: happy path - verify_signature False, enforce_minimum_key_length default
def test_get_sig_options_happy_path_default():
    py = _make_pyjwt({"verify_signature": False})
    assert py._get_sig_options() == {
        "verify_signature": False,
        "enforce_minimum_key_length": False,
    }

# curto: explicitamente set enforce_minimum_key_length and ignore extra keys
def test_get_sig_options_explicit_and_ignores_extra():
    py = _make_pyjwt({"verify_signature": True, "enforce_minimum_key_length": True, "extra": "x"})
    assert py._get_sig_options() == {
        "verify_signature": True,
        "enforce_minimum_key_length": True,
    }
