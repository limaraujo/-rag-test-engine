from repositorios.pyjwt.jwt.api_jwt import PyJWT

# default options matching the implementation's returned dictionary
_DEFAULT_OPTIONS = {
    "verify_signature": True,
    "verify_exp": True,
    "verify_nbf": True,
    "verify_iat": True,
    "verify_aud": True,
    "verify_iss": True,
    "verify_sub": True,
    "verify_jti": True,
    "require": [],
    "strict_aud": False,
    "enforce_minimum_key_length": False,
}

# short: happy path ensures default options are as expected
def test_get_default_options_happy_path():
    opts = PyJWT._get_default_options()
    assert isinstance(opts, dict)
    assert opts == _DEFAULT_OPTIONS

# short: verify that each call returns a new dict (no shared mutable state)
def test_get_default_options_returns_new_dict_each_call():
    a = PyJWT._get_default_options()
    b = PyJWT._get_default_options()
    assert a is not b
    assert a == b
