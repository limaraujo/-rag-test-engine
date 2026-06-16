import pytest
from repositorios.pyjwt.jwt import exceptions
from repositorios.pyjwt.jwt.api_jws import PyJWS

def test_validate_kid_raises_on_non_string():
    with pytest.raises(exceptions.InvalidTokenError):
        PyJWS._validate_kid(object(), 123)

def test_validate_kid_accepts_string_no_exception():
    assert PyJWS._validate_kid(object(), "kid123") is None
