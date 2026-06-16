from repositorios.pyjwt.jwt.api_jws import PyJWS

# curto: happy path - verifica retorno padrão de PyJWS._get_default_options
def test__get_default_options_returns_expected_defaults():
    options = PyJWS._get_default_options()
    assert isinstance(options, dict)
    assert options == {"verify_signature": True, "enforce_minimum_key_length": False}
