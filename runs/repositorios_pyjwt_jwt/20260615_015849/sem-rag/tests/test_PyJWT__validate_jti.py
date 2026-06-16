import pytest
from repositorios.pyjwt.jwt.exceptions import InvalidJTIError
from repositorios.pyjwt.jwt.api_jwt import PyJWT

import pytest

from repositorios.pyjwt.jwt.exceptions import InvalidJTIError
from repositorios.pyjwt.jwt.api_jwt import PyJWT

# short: happy path - jti is missing from payload, should not raise
def test__validate_jti_missing_key_no_exception():
    jwt = PyJWT.__new__(PyJWT)
    payload = {"iss": "issuer"}  # no 'jti' key
    jwt._validate_jti(payload)

# short: exception path - jti present but not a string, should raise
def test__validate_jti_non_string_raises():
    jwt = PyJWT.__new__(PyJWT)
    payload = {"jti": 12345}  # non-string jti
    with pytest.raises(InvalidJTIError):
        jwt._validate_jti(payload)

# short: happy path - jti present and is a string, should not raise
def test__validate_jti_string_no_exception():
    jwt = PyJWT.__new__(PyJWT)
    payload = {"jti": "abcd-1234"}  # valid string jti
    jwt._validate_jti(payload)
