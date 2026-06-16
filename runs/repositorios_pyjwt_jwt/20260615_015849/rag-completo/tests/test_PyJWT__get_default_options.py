from repositorios.pyjwt.jwt.api_jwt import PyJWT

EXPECTED_DEFAULT_OPTIONS = {
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

def _call_default_options():
    # Tenta chamar como método estático; se não for, cria uma instância sem init
    try:
        return PyJWT._get_default_options()
    except TypeError:
        obj = PyJWT.__new__(PyJWT)
        return PyJWT._get_default_options(obj)

# Verifica valores padrão corretos (caminho feliz)
def test_get_default_options_values_match_expected():
    opts = _call_default_options()
    assert isinstance(opts, dict)
    assert opts == EXPECTED_DEFAULT_OPTIONS

# Verifica independência entre chamadas (não compartilha estado)
def test_get_default_options_returns_new_dict_each_call():
    o1 = _call_default_options()
    o2 = _call_default_options()
    assert o1 is not o2
    o1["verify_signature"] = False
    assert o2["verify_signature"] is True

# Verifica chaves esperadas estão presentes (sem keys extras)
def test_get_default_options_keys_are_exact():
    opts = _call_default_options()
    assert set(opts.keys()) == set(EXPECTED_DEFAULT_OPTIONS.keys())
