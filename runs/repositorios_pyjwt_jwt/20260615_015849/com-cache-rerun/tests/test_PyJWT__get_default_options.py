from repositorios.pyjwt.jwt.api_jwt import PyJWT

# verifica valor padrão padrão e estrutura de opções (caminho feliz)
def test_get_default_options_happy_path_values():
    defaults = PyJWT._get_default_options()
    assert defaults["verify_signature"] is True
    assert defaults["verify_exp"] is True
    assert defaults["verify_nbf"] is True
    assert defaults["verify_iat"] is True
    assert defaults["verify_aud"] is True
    assert defaults["verify_iss"] is True
    assert defaults["verify_sub"] is True
    assert defaults["verify_jti"] is True
    assert defaults["require"] == []
    assert defaults["strict_aud"] is False
    assert defaults["enforce_minimum_key_length"] is False
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
    assert set(defaults.keys()) == expected_keys

# verifica que cada chamada retorna um dicionário distinto (imutabilidade/independência)
def test_get_default_options_returns_new_dict_each_call():
    o1 = PyJWT._get_default_options()
    o2 = PyJWT._get_default_options()
    o1["verify_signature"] = False
    assert o2["verify_signature"] is True

# verifica tipo da opção 'require' e conteúdo inicial
def test_get_default_options_require_is_list_and_empty_by_default():
    o = PyJWT._get_default_options()
    assert isinstance(o["require"], list)
    assert o["require"] == []
