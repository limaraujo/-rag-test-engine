from repositorios.pyjwt.jwt.api_jwt import PyJWT

# Verifica retorno direto de options quando None (happy path)
def test_merge_options_none_returns_existing_options():
    base_opts = {"verify_signature": True, "verify_exp": True}
    inst = PyJWT.__new__(PyJWT)
    inst.options = dict(base_opts)
    merged = inst._merge_options(None)
    assert merged is inst.options
    assert merged == inst.options

# Defensivo: quando verify_signature é False, defaults para verify_exp etc são definidas como False
def test_merge_options_defensive_defaults_when_verify_signature_false():
    inst = PyJWT.__new__(PyJWT)
    inst.options = {
        "verify_signature": True,
        "verify_exp": True,
        "verify_nbf": True,
        "verify_iat": True,
        "verify_aud": True,
        "verify_iss": True,
        "verify_sub": True,
        "verify_jti": True,
    }
    input_opts = {"verify_signature": False}
    merged = inst._merge_options(input_opts)
    assert merged["verify_signature"] is False
    for k in (
        "verify_exp",
        "verify_nbf",
        "verify_iat",
        "verify_aud",
        "verify_iss",
        "verify_sub",
        "verify_jti",
    ):
        assert merged[k] is False

# Verifica que quando verify_signature é True, não alteramos defaults por omission
def test_merge_options_preserves_existing_when_verify_signature_true_and_no_overrides():
    inst = PyJWT.__new__(PyJWT)
    inst.options = {
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
    }
    input_opts = {"verify_signature": True}
    merged = inst._merge_options(input_opts)
    assert merged["verify_signature"] is True
    assert merged["verify_exp"] is True
    assert merged["verify_nbf"] is True

# Verifica que falhas de override explícito funcionam (ex.: verify_exp removido)
def test_merge_options_explicit_override_overrides_existing_values():
    inst = PyJWT.__new__(PyJWT)
    inst.options = {
        "verify_signature": True,
        "verify_exp": True,
        "verify_nbf": True,
    }
    input_opts = {"verify_signature": True, "verify_exp": False}
    merged = inst._merge_options(input_opts)
    assert merged["verify_signature"] is True
    assert merged["verify_exp"] is False
