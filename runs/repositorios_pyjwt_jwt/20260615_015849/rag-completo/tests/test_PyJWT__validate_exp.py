import pytest
from repositorios.pyjwt.jwt.exceptions import DecodeError, ExpiredSignatureError
from repositorios.pyjwt.jwt.api_jwt import PyJWT

# Verifica caminho feliz (exp > now - leeway) não lança exceção
def test_validate_exp_happy_path():
    obj = PyJWT.__new__(PyJWT)
    payload = {"exp": "1010"}
    now = 1000
    leeway = 60
    PyJWT._validate_exp(obj, payload, now, leeway)

# Verifica lança DecodeError quando exp não pode ser convertido para inteiro
def test_validate_exp_decodeerror_on_invalid_exp():
    obj = PyJWT.__new__(PyJWT)
    payload = {"exp": "not-an-int"}
    now = 1000
    leeway = 0
    with pytest.raises(DecodeError):
        PyJWT._validate_exp(obj, payload, now, leeway)

# Verifica ExpiredSignatureError quando exp é menor ou igual a now - leeway
def test_validate_exp_expired_signature_error():
    obj = PyJWT.__new__(PyJWT)
    payload = {"exp": "995"}  # 995 <= (1000 - 5) = 995
    now = 1000
    leeway = 5
    with pytest.raises(ExpiredSignatureError):
        PyJWT._validate_exp(obj, payload, now, leeway)
