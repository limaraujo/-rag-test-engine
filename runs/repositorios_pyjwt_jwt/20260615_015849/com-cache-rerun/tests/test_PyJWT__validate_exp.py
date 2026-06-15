import pytest
from repositorios.pyjwt.jwt.exceptions import DecodeError, ExpiredSignatureError
from repositorios.pyjwt.jwt.api_jwt import PyJWT

def _make_instance():
    return PyJWT.__new__(PyJWT)

# verifica caminho feliz: exp compatível e token ainda válido (não lança)
def test_validate_exp_happy_path():
    obj = _make_instance()
    payload = {"exp": 1010}
    now = 1000
    leeway = 10
    obj._validate_exp(payload, now, leeway)

# verifica caso exp expirou: exp <= now - leeway levanta ExpiredSignatureError
def test_validate_exp_expired():
    obj = _make_instance()
    payload = {"exp": 990}
    now = 1000
    leeway = 10
    with pytest.raises(ExpiredSignatureError):
        obj._validate_exp(payload, now, leeway)

# verifica erro ao parsear exp não inteiro: levanta DecodeError
def test_validate_exp_invalid_int():
    obj = _make_instance()
    payload = {"exp": "not_an_int"}
    now = 1000
    leeway = 0
    with pytest.raises(DecodeError):
        obj._validate_exp(payload, now, leeway)

# verifica comportamento ao faltar a claim exp: KeyError é propagado
def test_validate_exp_missing_key_raises_keyerror():
    obj = _make_instance()
    payload = {}
    now = 1000
    leeway = 0
    with pytest.raises(KeyError):
        obj._validate_exp(payload, now, leeway)
