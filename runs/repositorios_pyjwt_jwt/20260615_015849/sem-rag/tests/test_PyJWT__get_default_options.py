from repositorios.pyjwt.jwt.api_jwt import PyJWT

# Verifica o caminho feliz: retorna opções padrão exatamente com os valores esperados
def test_get_default_options_happy_path():
    expected = {
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
    assert PyJWT._get_default_options() == expected

# Verifica que cada chamada retorna um novo dict (não o mesmo objeto)
def test_get_default_options_returns_new_dict_each_call():
    a = PyJWT._get_default_options()
    b = PyJWT._get_default_options()
    assert a == b
    assert a is not b

# Verifica que mutação de retorno não afeta chamadas futuras (isolamento de cópia)
def test_get_default_options_mutation_does_not_affect_future_calls():
    a = PyJWT._get_default_options()
    a["verify_signature"] = False
    c = PyJWT._get_default_options()
    assert c["verify_signature"] is True
