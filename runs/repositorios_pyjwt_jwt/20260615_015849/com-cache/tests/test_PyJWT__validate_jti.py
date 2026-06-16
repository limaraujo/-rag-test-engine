import pytest
from repositorios.pyjwt.jwt.exceptions import InvalidJTIError
from repositorios.pyjwt.jwt.api_jwt import PyJWT

import pytest

from repositorios.pyjwt.jwt.exceptions import InvalidJTIError
from repositorios.pyjwt.jwt.api_jwt import PyJWT

# curto: verifica que não ocorre erro quando 'jti' não está no payload
def test_validate_jti_missing_key_no_error():
    payload = {"iss": "issuer"}
    self = PyJWT.__new__(PyJWT)
    PyJWT._validate_jti(self, payload)

# curto: verifica que InvalidJTIError é levantada quando 'jti' não é string
def test_validate_jti_non_string_raises():
    payload = {"jti": 123}
    self = PyJWT.__new__(PyJWT)
    with pytest.raises(InvalidJTIError, match="JWT ID must be a string"):
        PyJWT._validate_jti(self, payload)

# curto: verifica que quando 'jti' é string, não levanta exceção
def test_validate_jti_string_no_error():
    payload = {"jti": "valid-jti"}
    self = PyJWT.__new__(PyJWT)
    PyJWT._validate_jti(self, payload)
