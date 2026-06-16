from repositorios.pyjwt.jwt.exceptions import InvalidIssuedAtError, ImmatureSignatureError
import pytest
from repositorios.pyjwt.jwt.api_jwt import PyJWT

# teste: happy path — iat dentro do intervalo permitido (não lança)
def test_validate_iat_happy_path_no_exception():
    jwt = PyJWT()
    payload = {"iat": "1000"}
    now = 1005
    leeway = 5
    jwt._validate_iat(payload, now, leeway)

# teste: exceção para input inválido no iat (não numérico)
def test_validate_iat_invalid_input_raises_InvalidIssuedAtError():
    jwt = PyJWT()
    payload = {"iat": "not-a-number"}
    now = 1000
    leeway = 10
    with pytest.raises(InvalidIssuedAtError):
        jwt._validate_iat(payload, now, leeway)

# teste: branch imatura — iat no futuro além do leeway
def test_validate_iat_immature_signature_raises_ImmatureSignatureError():
    jwt = PyJWT()
    payload = {"iat": "1011"}
    now = 1000
    leeway = 5  # now + leeway = 1005; 1011 > 1005
    with pytest.raises(ImmatureSignatureError):
        jwt._validate_iat(payload, now, leeway)
