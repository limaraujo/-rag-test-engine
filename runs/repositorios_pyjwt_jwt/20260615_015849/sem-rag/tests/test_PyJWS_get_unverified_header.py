import pytest
from repositorios.pyjwt.jwt.api_jws import PyJWS

# happy path: header dict returned and _load receives the input jwt type
@pytest.mark.parametrize("jwt_input", ["header.jwt", b"header.jwt"])
def test_get_unverified_header_happy_path_preserves_jwt_type_and_returns_headers(jwt_input):
    pyjws = PyJWS.__new__(PyJWS)
    loaded = []
    validated = []

    def _load(jwt):
        loaded.append(jwt)
        return (None, None, {'typ': 'JWT', 'alg': 'HS256'})

    def _validate_headers(headers):
        validated.append(headers)

    pyjws._load = _load
    pyjws._validate_headers = _validate_headers

    headers = pyjws.get_unverified_header(jwt_input)

    assert headers == {'typ': 'JWT', 'alg': 'HS256'}
    assert len(loaded) == 1
    assert type(loaded[0]) is type(jwt_input) and loaded[0] == jwt_input
    assert validated == [headers]

# exception path: propagate exception from _validate_headers
def test_get_unverified_header_propagates_exception_from_validate_headers():
    pyjws = PyJWS.__new__(PyJWS)
    def _load(jwt):
        return (None, None, {'typ': 'JWT', 'alg': 'HS256'})

    def _validate_headers(headers):
        raise ValueError("bad headers")

    pyjws._load = _load
    pyjws._validate_headers = _validate_headers

    with pytest.raises(ValueError, match="bad headers"):
        pyjws.get_unverified_header("any jwt")
