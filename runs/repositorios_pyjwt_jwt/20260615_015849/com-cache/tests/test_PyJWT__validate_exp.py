import pytest
from repositorios.pyjwt.jwt.exceptions import DecodeError, ExpiredSignatureError
from repositorios.pyjwt.jwt.api_jwt import PyJWT

# verifica caminho feliz: exp é after current time considering leeway (não levanta exceção)
def test_validate_exp_happy_path_no_exception():
    inst = PyJWT.__new__(PyJWT)
    payload = {"exp": 999999}
    now = 1000.0
    leeway = 10.0
    inst._validate_exp(payload, now, leeway)

# verifica falha por expiração: exp <= now - leeway deve raise ExpiredSignatureError
def test_validate_exp_expired_signature_raised():
    inst = PyJWT.__new__(PyJWT)
    payload = {"exp": 50}
    now = 100.0
    leeway = 10.0
    with pytest.raises(ExpiredSignatureError):
        inst._validate_exp(payload, now, leeway)

# verifica input inválido: exp não é convertido para inteiro -> raise DecodeError
def test_validate_exp_invalid_type_decodeerror():
    inst = PyJWT.__new__(PyJWT)
    payload = {"exp": "not_an_int"}
    now = 100.0
    leeway = 10.0
    with pytest.raises(DecodeError):
        inst._validate_exp(payload, now, leeway)
