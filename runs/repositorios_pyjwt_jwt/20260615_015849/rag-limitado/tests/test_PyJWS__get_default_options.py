from repositorios.pyjwt.jwt.api_jws import PyJWS

# teste feliz: verificar retorno exato do dicionário de opções padrão
def test_get_default_options_happy_path():
    assert PyJWS._get_default_options() == {
        "verify_signature": True,
        "enforce_minimum_key_length": False,
    }

# teste de estrutura e conteúdo: retorna dict com as chaves esperadas
def test_get_default_options_type_and_keys():
    opts = PyJWS._get_default_options()
    assert isinstance(opts, dict)
    assert set(opts.keys()) == {"verify_signature", "enforce_minimum_key_length"}
    assert opts["verify_signature"] is True
    assert opts["enforce_minimum_key_length"] is False

# teste de independência de chamadas: cada chamada retorna novo dict
def test_get_default_options_calls_return_new_dict():
    o1 = PyJWS._get_default_options()
    o2 = PyJWS._get_default_options()
    assert o1 is not o2
    assert o1 == o2
