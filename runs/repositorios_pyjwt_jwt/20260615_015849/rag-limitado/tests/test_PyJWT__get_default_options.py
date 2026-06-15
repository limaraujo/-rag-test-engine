from repositorios.pyjwt.jwt.api_jwt import PyJWT

def test_get_default_options_happy_path_matches_expected():
    opts = PyJWT._get_default_options()
    expected = {
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
    assert opts == expected

def test_get_default_options_keys_and_types():
    opts = PyJWT._get_default_options()
    expected_keys = {
        "verify_signature",
        "verify_exp",
        "verify_nbf",
        "verify_iat",
        "verify_aud",
        "verify_iss",
        "verify_sub",
        "verify_jti",
        "require",
        "strict_aud",
        "enforce_minimum_key_length",
    }
    assert set(opts.keys()) == expected_keys
    assert isinstance(opts["require"], list)
    assert isinstance(opts["verify_signature"], bool)
    assert isinstance(opts["strict_aud"], bool)
    assert isinstance(opts["enforce_minimum_key_length"], bool)

def test_get_default_options_returns_new_dict_each_call():
    first = PyJWT._get_default_options()
    second = PyJWT._get_default_options()
    assert first is not second
    assert first == second
