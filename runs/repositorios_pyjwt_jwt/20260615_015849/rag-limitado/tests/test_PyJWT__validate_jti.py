from repositorios.pyjwt.jwt.exceptions import InvalidJTIError
import pytest
from repositorios.pyjwt.jwt.api_jwt import PyJWT

# Verifica o caminho feliz: ausência de 'jti' não levanta exceção
def test__validate_jti_missing_key_no_error():
    jwt = PyJWT.__new__(PyJWT)
    payload = {"sub": "user1"}  # não contém 'jti'
    jwt._validate_jti(payload)

# Verifica exceção quando 'jti' não é string
def test__validate_jti_non_string_raises():
    jwt = PyJWT.__new__(PyJWT)
    payload = {"jti": 123}  # 'jti' não é string
    with pytest.raises(InvalidJTIError):
        jwt._validate_jti(payload)

# Verifica o caminho feliz: 'jti' é string válida
def test__validate_jti_string_no_error():
    jwt = PyJWT.__new__(PyJWT)
    payload = {"jti": "abc123"}  # 'jti' é string
    jwt._validate_jti(payload)
