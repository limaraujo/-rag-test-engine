from repositorios.pyjwt.jwt.api_jws import PyJWS

# short: happy path test - default options structure and exact values
def test_get_default_options_happy_path():
    # verifique que o retorno corresponde ao dicionário de opções padrão
    opts = PyJWS._get_default_options()
    assert isinstance(opts, dict)
    assert opts == {"verify_signature": True, "enforce_minimum_key_length": False}

# short: structure and type checks for default options
def test_get_default_options_keys_and_values():
    # assegure que as chaves e tipos de valores são corretos
    opts = PyJWS._get_default_options()
    assert set(opts.keys()) == {"verify_signature", "enforce_minimum_key_length"}
    assert opts["verify_signature"] is True
    assert opts["enforce_minimum_key_length"] is False
