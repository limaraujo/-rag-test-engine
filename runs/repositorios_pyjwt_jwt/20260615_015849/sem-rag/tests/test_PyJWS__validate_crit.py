from repositorios.pyjwt.jwt.exceptions import InvalidTokenError
import pytest
from repositorios.pyjwt.jwt.api_jws import PyJWS

def _make_instance():
    inst = object.__new__(PyJWS)
    inst._supported_crit = {"exp", "nbf", "aud"}
    return inst

# happy path: valid crit list entries present in headers
def test_validate_crit_happy_path():
    inst = _make_instance()
    headers = {"crit": ["exp", "nbf"], "exp": "1", "nbf": "2"}
    inst._validate_crit(headers)

# edge: invalid 'crit' header structure (empty or non-list)
@pytest.mark.parametrize("crit", [[], "notalist"])
def test_validate_crit_invalid_crit_header_structure(crit):
    inst = _make_instance()
    headers = {"crit": crit}
    with pytest.raises(InvalidTokenError):
        inst._validate_crit(headers)

# edge: crit entries must be strings
def test_validate_crit_non_string_ext_values():
    inst = _make_instance()
    headers = {"crit": [1]}
    with pytest.raises(InvalidTokenError, match="values must be strings"):
        inst._validate_crit(headers)

# branches: either unsupported extension or missing header for a valid ext
@pytest.mark.parametrize("crit,expected", [
    (["unknown"], "Unsupported critical extension: unknown"),
    (["exp"], "Critical extension 'exp' is missing from headers"),
])
def test_validate_crit_unsupported_or_missing_header(crit, expected):
    inst = _make_instance()
    headers = {"crit": crit}
    with pytest.raises(InvalidTokenError, match=expected):
        inst._validate_crit(headers)
