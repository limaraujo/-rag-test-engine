from repositorios.pyjwt.jwt.exceptions import InvalidJTIError
import pytest
from repositorios.pyjwt.jwt.api_jwt import PyJWT

# curto: branch (jti ausente) — valida o caminho feliz sem jti
def test_validate_jti_missing_key_no_exception():
    jwt = PyJWT()
    payload = {"sub": "user_123"}
    jwt._validate_jti(payload)

# curto: happy path — jti presente como string não levanta exceção
def test_validate_jti_string_no_exception():
    jwt = PyJWT()
    payload = {"jti": "token-id-456"}
    jwt._validate_jti(payload)

# curto: exceção listada — jti presente mas não é string levanta InvalidJTIError
def test_validate_jti_non_string_raises_InvalidJTIError():
    jwt = PyJWT()
    payload = {"jti": 789}
    with pytest.raises(InvalidJTIError):
        jwt._validate_jti(payload)
