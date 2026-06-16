from repositorios.pyjwt.jwt.api_jwt import PyJWT

def _make_pyjwt_with_options(opts: dict) -> PyJWT:
    pyjwt = PyJWT.__new__(PyJWT)
    pyjwt.options = opts
    return pyjwt

# Verifica retorno quando ambas chaves estão presentes (caminho feliz)
def test_get_sig_options_both_keys_present():
    pyjwt = _make_pyjwt_with_options({"verify_signature": True, "enforce_minimum_key_length": True})
    assert pyjwt._get_sig_options() == {
        "verify_signature": True,
        "enforce_minimum_key_length": True,
    }

# Verifica valor padrão de enforce_minimum_key_length quando ausente (caso de borda)
def test_get_sig_options_defaults_enforce_min_length_missing():
    pyjwt = _make_pyjwt_with_options({"verify_signature": False})
    assert pyjwt._get_sig_options() == {
        "verify_signature": False,
        "enforce_minimum_key_length": False,
    }

# Verifica comportamento com verify_signature=False mantendo a configuração de enforce_minimum_key_length
def test_get_sig_options_verify_signature_false():
    pyjwt = _make_pyjwt_with_options({"verify_signature": False, "enforce_minimum_key_length": False})
    assert pyjwt._get_sig_options() == {
        "verify_signature": False,
        "enforce_minimum_key_length": False,
    }
