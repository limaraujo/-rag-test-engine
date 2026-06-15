from repositorios.pyjwt.jwt.api_jwt import PyJWT

# short: happy path - options is None should return the current self.options
def test_merge_options_none_returns_current_options():
    obj = PyJWT.__new__(PyJWT)
    obj.options = {'verify_signature': True, 'verify_exp': True, 'require': [], 'custom': 'X'}
    res = obj._merge_options(None)
    assert res is obj.options

# short: branch - when verify_signature is False, defaults for verify_* are set to False
def test_merge_options_defensive_defaults_when_verify_signature_false():
    obj = PyJWT.__new__(PyJWT)
    obj.options = {
        'verify_signature': True,
        'verify_exp': True,
        'verify_nbf': True,
        'verify_iat': True,
        'verify_aud': True,
        'verify_iss': True,
        'verify_sub': True,
        'verify_jti': True,
        'require': ['aud'],
        'custom': 'A'
    }
    options = {'verify_signature': False}
    res = obj._merge_options(options)
    for key in ['verify_signature', 'verify_exp', 'verify_nbf', 'verify_iat',
                'verify_aud', 'verify_iss', 'verify_sub', 'verify_jti']:
        assert res[key] is False
    assert res['require'] == ['aud']
    assert res['custom'] == 'A'

# short: branch not taken - when verify_signature is True, explicit options override defaults
def test_merge_options_defensive_not_triggered_when_verify_signature_true():
    obj = PyJWT.__new__(PyJWT)
    obj.options = {
        'verify_signature': False,
        'verify_exp': False,
        'verify_nbf': False,
        'verify_iat': False,
        'verify_iss': False,
        'verify_jti': False,
        'require': [],
        'custom': 'B'
    }
    options = {'verify_signature': True, 'verify_exp': True}
    res = obj._merge_options(options)
    assert res['verify_signature'] is True
    assert res['verify_exp'] is True
    assert res['verify_nbf'] is False
    assert res['custom'] == 'B'
    assert res['require'] == []
