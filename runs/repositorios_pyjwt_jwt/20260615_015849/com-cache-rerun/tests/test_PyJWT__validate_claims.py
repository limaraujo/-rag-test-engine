import pytest
from datetime import timedelta
from types import MethodType
from repositorios.pyjwt.jwt.api_jwt import PyJWT


# Verifica o caminho feliz: todas as validações são chamadas quando claims existem e leeway é convertido de timedelta
def test_validate_claims_calls_all_validations_and_leeway_conversion():
    instance = PyJWT.__new__(PyJWT)

    captured = {}

    def _validate_required_claims(self, payload, require):
        captured['required'] = require

    def _validate_iat(self, payload, now, leeway):
        captured['iat'] = {'now': now, 'leeway': leeway}

    def _validate_nbf(self, payload, now, leeway):
        captured['nbf'] = True

    def _validate_exp(self, payload, now, leeway):
        captured['exp'] = True

    def _validate_iss(self, payload, issuer):
        captured['iss'] = issuer

    def _validate_aud(self, payload, audience, strict=False):
        captured['aud'] = {'audience': audience, 'strict': strict}

    def _validate_sub(self, payload, subject):
        captured['sub'] = subject

    def _validate_jti(self, payload):
        captured['jti'] = True

    instance._validate_required_claims = MethodType(_validate_required_claims, instance)
    instance._validate_iat = MethodType(_validate_iat, instance)
    instance._validate_nbf = MethodType(_validate_nbf, instance)
    instance._validate_exp = MethodType(_validate_exp, instance)
    instance._validate_iss = MethodType(_validate_iss, instance)
    instance._validate_aud = MethodType(_validate_aud, instance)
    instance._validate_sub = MethodType(_validate_sub, instance)
    instance._validate_jti = MethodType(_validate_jti, instance)

    payload = {'iat': 1, 'nbf': 2, 'exp': 3, 'iss': 'issuer', 'aud': 'aud', 'sub': 'sub', 'jti': 'id'}
    options = {
        "require": [],
        "verify_iat": True,
        "verify_nbf": True,
        "verify_exp": True,
        "verify_iss": True,
        "verify_aud": True,
        "verify_sub": True,
        "verify_jti": True,
        "strict_aud": False,
    }

    audience = "aud"
    issuer = "issuer"
    subject = "sub"
    leeway = timedelta(seconds=5)

    instance._validate_claims(payload, options, audience=audience, issuer=issuer, subject=subject, leeway=leeway)

    assert captured['required'] == []
    assert 'iat' in captured and captured['iat']['leeway'] == 5.0
    assert captured.get('nbf') is True
    assert captured.get('exp') is True
    assert captured.get('iss') == issuer
    assert captured.get('aud') == {'audience': audience, 'strict': False}
    assert captured.get('sub') == subject
    assert captured.get('jti') is True


# Verifica que TypeError é levantado quando audience não é string/iterable/nulo
def test_validate_claims_audience_type_error():
    instance = PyJWT.__new__(PyJWT)
    payload = {'exp': 1}
    options = {
        "require": [],
        "verify_iat": False,
        "verify_nbf": False,
        "verify_exp": True,
        "verify_iss": False,
        "verify_aud": False,
        "verify_sub": False,
        "verify_jti": False,
        "strict_aud": False,
    }

    with pytest.raises(TypeError):
        instance._validate_claims(payload, options, audience=123)


# Verifica que apenas o exp é chamado quando apenas exp está presente e enabled
def test_validate_claims_only_exp_called_when_present_and_only_exp_enabled():
    instance = PyJWT.__new__(PyJWT)
    captured = {}

    def _validate_exp(self, payload, now, leeway):
        captured['exp'] = True

    def _validate_iat(self, payload, now, leeway):
        captured['iat'] = True

    def _validate_iss(self, payload, issuer):
        captured['iss'] = True

    def _validate_aud(self, payload, audience, strict=False):
        captured['aud'] = True

    def _validate_sub(self, payload, subject):
        captured['sub'] = True

    def _validate_jti(self, payload):
        captured['jti'] = True

    instance._validate_required_claims = MethodType(lambda self, payload, require: None, instance)
    instance._validate_exp = MethodType(_validate_exp, instance)
    instance._validate_iat = MethodType(_validate_iat, instance)
    instance._validate_iss = MethodType(_validate_iss, instance)
    instance._validate_aud = MethodType(_validate_aud, instance)
    instance._validate_sub = MethodType(_validate_sub, instance)
    instance._validate_jti = MethodType(_validate_jti, instance)

    payload = {'exp': 1}
    options = {
        "require": [],
        "verify_iat": False,
        "verify_nbf": False,
        "verify_exp": True,
        "verify_iss": False,
        "verify_aud": False,
        "verify_sub": False,
        "verify_jti": False,
        "strict_aud": False,
    }

    instance._validate_claims(payload, options)

    assert captured.get('exp') is True
    assert captured.get('iat') is None
    assert captured.get('iss') is None
    assert captured.get('aud') is None
    assert captured.get('sub') is None
    assert captured.get('jti') is None
