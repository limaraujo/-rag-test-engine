import pytest
from repositorios.pyjwt.jwt.exceptions import InvalidTokenError
from repositorios.pyjwt.jwt.api_jws import PyJWS

# happy path: kid is a string, no exception raised
def test_validate_kid_accepts_string_no_exception():
    # short: ensure no error for valid string kid
    pyjws = PyJWS.__new__(PyJWS)
    pyjws._validate_kid("validKid")

# exception path: non-string kid raises InvalidTokenError
def test_validate_kid_raises_on_non_string_kid():
    # short: ensure InvalidTokenError when kid is not a string
    pyjws = PyJWS.__new__(PyJWS)
    with pytest.raises(InvalidTokenError, match="Key ID header parameter must be a string"):
        pyjws._validate_kid(123)
