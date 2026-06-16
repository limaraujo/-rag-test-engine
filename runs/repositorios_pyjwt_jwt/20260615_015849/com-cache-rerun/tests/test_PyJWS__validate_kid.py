import pytest
from repositorios.pyjwt.jwt.exceptions import InvalidTokenError
from repositorios.pyjwt.jwt.api_jws import PyJWS

# Verifica o caminho feliz: kid é string não levanta exceção
def test_validate_kid_accepts_string_no_exception():
    PyJWS._validate_kid(None, "kid123")

# Verifica tratamento de tipos não-string para kid
@pytest.mark.parametrize("kid", [None, 123, 12.5, [], {}])
def test_validate_kid_raises_on_non_string(kid):
    with pytest.raises(InvalidTokenError) as excinfo:
        PyJWS._validate_kid(None, kid)
    assert "Key ID header parameter must be a string" in str(excinfo.value)
