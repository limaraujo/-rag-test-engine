import pytest
from repositorios.pyjwt.jwt.exceptions import InvalidTokenError
from repositorios.pyjwt.jwt.api_jws import PyJWS

class _Dummy:
    def __init__(self, supported_crit):
        self._supported_crit = supported_crit

# curto: happy path when crit is valid and header contains the required extension
def test_validate_crit_happy_path():
    dummy = _Dummy({'exp'})
    headers = {'crit': ['exp'], 'exp': 'value'}
    PyJWS._validate_crit(dummy, headers)

# curto: invalid 'crit' header type or empty collection
@pytest.mark.parametrize("crit_value", ["not-a-list", [], None])
def test_validate_crit_invalid_crit_header(crit_value):
    dummy = _Dummy({'exp'})
    headers = {'crit': crit_value}
    with pytest.raises(InvalidTokenError):
        PyJWS._validate_crit(dummy, headers)

# curto: unsupported critical extension triggers error
def test_validate_crit_unsupported_extension():
    dummy = _Dummy({'exp'})
    headers = {'crit': ['x']}
    with pytest.raises(InvalidTokenError) as exc:
        PyJWS._validate_crit(dummy, headers)
    assert "Unsupported critical extension: x" in str(exc.value)

# curto: missing required header for a supported extension triggers error
def test_validate_crit_missing_header_for_extension():
    dummy = _Dummy({'exp'})
    headers = {'crit': ['exp']}  # 'exp' not present in headers
    with pytest.raises(InvalidTokenError) as exc:
        PyJWS._validate_crit(dummy, headers)
    assert "Critical extension 'exp' is missing from headers" in str(exc.value)
