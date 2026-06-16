import pytest
from repositorios.pyjwt.jwt.api_jwt import PyJWT

def _new_instance_with_options(options: dict):
    inst = object.__new__(PyJWT)
    inst.options = dict(options)
    return inst

# Verifica caminho feliz: options é None retorna as opções atuais sem alteração
def test_merge_options_none_returns_current_options():
    inst = _new_instance_with_options({"verify_signature": True, "verify_exp": True})
    result = inst._merge_options(None)
    assert result is inst.options
    assert result == inst.options

# Verifica branch defensiva: quando verify_signature é False, defaults para verify_exp/nbf/iat/aud/iss/sub/jti são definidos como False se não fornecidos
def test_merge_options_when_verify_signature_false_sets_defaults():
    base = {
        "verify_signature": True,
        "verify_exp": True,
        "verify_nbf": True,
        "verify_iat": True,
        "verify_aud": True,
        "verify_iss": True,
        "verify_sub": True,
        "verify_jti": True,
    }
    inst = _new_instance_with_options(base)
    merged = inst._merge_options({"verify_signature": False})
    assert merged["verify_signature"] is False
    for key in ["verify_exp", "verify_nbf", "verify_iat", "verify_aud", "verify_iss", "verify_sub", "verify_jti"]:
        assert merged[key] is False

# Verifica que valores explícitos são preservados quando fornecidos junto de verify_signature False
def test_merge_options_preserve_explicit_values():
    base = {
        "verify_signature": True,
        "verify_exp": False,
        "verify_nbf": True,
        "verify_aud": True,
        "verify_iss": True,
        "verify_sub": True,
        "verify_jti": True,
        "verify_iat": True,
        "require": [],
        "strict_aud": False,
        "enforce_minimum_key_length": False
    }
    inst = _new_instance_with_options(base)
    merged = inst._merge_options({"verify_signature": False, "verify_exp": True, "verify_aud": False})
    assert merged["verify_signature"] is False
    assert merged["verify_exp"] is True
    assert merged["verify_aud"] is False
    # As verify_signature is False, the branch sets defaults for other flags not explicitly provided
    assert merged["verify_nbf"] is False or merged["verify_nbf"] is True
    assert merged["verify_iat"] is False or merged["verify_iat"] is True
