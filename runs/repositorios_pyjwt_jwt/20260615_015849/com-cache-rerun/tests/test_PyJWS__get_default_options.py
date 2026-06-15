from repositorios.pyjwt.jwt.api_jws import PyJWS

# curto: happy path - retorna o dicionário de opções padrão esperado
def test_get_default_options_returns_expected():
    opts = PyJWS._get_default_options()
    assert isinstance(opts, dict)
    assert opts == {"verify_signature": True, "enforce_minimum_key_length": False}
    assert set(opts.keys()) == {"verify_signature", "enforce_minimum_key_length"}

# curto: branch/independência entre chamadas - cada chamada deve retornar novo dict com o mesmo conteúdo
def test_get_default_options_returns_new_dict_each_call():
    first = PyJWS._get_default_options()
    second = PyJWS._get_default_options()
    assert first == second
    assert first is not second

# curto: não altera o retorno entre mutações locais - confirma independência entre instâncias
def test_get_default_options_independent_after_mutation():
    opts1 = PyJWS._get_default_options()
    opts1["verify_signature"] = False
    opts2 = PyJWS._get_default_options()
    assert opts2["verify_signature"] is True
