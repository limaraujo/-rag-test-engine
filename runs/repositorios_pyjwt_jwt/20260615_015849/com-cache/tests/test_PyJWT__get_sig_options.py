import pytest
from repositorios.pyjwt.jwt.api_jwt import PyJWT



# curto: helper to create PyJWT-like instance without running __init__
def _make_jwt_with_options(opts: dict) -> PyJWT:
    jwt = PyJWT.__new__(PyJWT)
    jwt.options = opts
    return jwt


# curto: happy path: verifique que _get_sig_options retorna valores diretos das opções presentes
def test_sig_options_happy_path():
    jwt = _make_jwt_with_options({"verify_signature": True, "enforce_minimum_key_length": True})
    assert jwt._get_sig_options() == {
        "verify_signature": True,
        "enforce_minimum_key_length": True,
    }


# curto: padrão de fallback para enforce_minimum_key_length quando ausente
def test_sig_options_default_enforce_minimum_false():
    jwt = _make_jwt_with_options({"verify_signature": False})
    assert jwt._get_sig_options() == {
        "verify_signature": False,
        "enforce_minimum_key_length": False,
    }


# curto: comportamento de erro quando verify_signature não está presente
def test_sig_options_missing_verify_signature_keyerror():
    jwt = _make_jwt_with_options({})
    with pytest.raises(KeyError):
        jwt._get_sig_options()


# curto: cenário adicional: verificar valor False explícito de verify_signature
def test_sig_options_explicit_false_verify_signature():
    jwt = _make_jwt_with_options({"verify_signature": False, "enforce_minimum_key_length": False})
    assert jwt._get_sig_options() == {
        "verify_signature": False,
        "enforce_minimum_key_length": False,
    }
