import pytest
from repositorios.pyjwt.jwt.exceptions import InvalidTokenError
from repositorios.pyjwt.jwt.api_jws import PyJWS

# Verifica happy path: kid é string e não levanta exceção
def test_validate_kid_accepts_string():
    pyjws = PyJWS.__new__(PyJWS)
    assert pyjws._validate_kid("kid-123") is None

# Verifica exceção: kid não é string e deve levantar InvalidTokenError
def test_validate_kid_raises_on_non_string():
    pyjws = PyJWS.__new__(PyJWS)
    with pytest.raises(InvalidTokenError):
        pyjws._validate_kid(123)
