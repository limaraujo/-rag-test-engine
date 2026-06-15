from repositorios.pyjwt.jwt.api_jwt import PyJWT

class DummyPyJWT(PyJWT):
    def __init__(self, options=None):
        self.options = options or {}

# Test 1: happy path (options is None) returns the current self.options
# happy path: options None -> retorna self.options sem alterações
def test_merge_options_none_returns_self_options():
    jwt = DummyPyJWT(options={'verify_signature': True, 'verify_exp': True, 'foo': 'bar'})
    result = jwt._merge_options(None)
    assert result is jwt.options
    assert result['verify_signature'] is True

# Test 2: branch when verify_signature is False and keys are missing -> defaults to False
# branch: verify_signature False com keys ausentes -> defaults para verify_* são False
def test_merge_options_defensive_defaults_when_verify_signature_false_and_missing_keys():
    base = {'verify_signature': True, 'foo': 'bar', 'verify_exp': True}
    jwt = DummyPyJWT(options=base)
    provided = {'verify_signature': False}
    result = jwt._merge_options(provided)
    expected = {
        'verify_signature': False,
        'verify_exp': False,
        'verify_nbf': False,
        'verify_iat': False,
        'verify_aud': False,
        'verify_iss': False,
        'verify_sub': False,
        'verify_jti': False,
        'foo': 'bar',
    }
    assert result == expected
    # self.options não deve ser mutate
    assert jwt.options['verify_exp'] is True

# Test 3: branch when verify_signature is False and explicit overrides are provided
# branch: verify_signature False com overrides fornecidos -> somente overrides prevalecem
def test_merge_options_defensive_defaults_with_overrides_when_verify_signature_false():
    base = {'verify_signature': True, 'verify_exp': False, 'foo': 'bar'}
    jwt = DummyPyJWT(options=base)
    provided = {'verify_signature': False, 'verify_exp': True}
    result = jwt._merge_options(provided)
    expected = {
        'verify_signature': False,
        'verify_exp': True,
        'verify_nbf': False,
        'verify_iat': False,
        'verify_aud': False,
        'verify_iss': False,
        'verify_sub': False,
        'verify_jti': False,
        'foo': 'bar',
    }
    assert result == expected
    assert jwt.options['verify_signature'] is True

# Test 4: default path (verify_signature is True) merges normally without changing missing keys
# happy path: verify_signature True -> merge simples sem Defaults adicionais
def test_merge_options_simple_merge_when_verify_signature_true():
    base = {'verify_signature': True, 'verify_exp': False, 'foo': 'bar'}
    jwt = DummyPyJWT(options=base)
    provided = {'verify_signature': True}
    result = jwt._merge_options(provided)
    expected = {'verify_signature': True, 'verify_exp': False, 'foo': 'bar'}
    assert result == expected
    assert jwt.options == base
