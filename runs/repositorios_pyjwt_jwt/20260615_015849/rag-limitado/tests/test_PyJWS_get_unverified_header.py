import pytest
from repositorios.pyjwt.jwt.api_jws import PyJWS

# short: happy path - returns unverified header and calls validation
def test_get_unverified_header_happy_path_calls_validate(monkeypatch):
    monkeypatch.setattr(PyJWS, "__init__", lambda self: None)
    jws = PyJWS()
    headers = {"alg": "HS256", "typ": "JWT"}
    jws._load = lambda jwt: (None, None, headers)
    captured = {}

    def mock_validate(h):
        captured["headers"] = h

    jws._validate_headers = mock_validate

    result = jws.get_unverified_header("token")

    assert result is headers
    assert captured["headers"] is headers

# short: exception from validation is propagated
def test_get_unverified_header_propagates_exception_from_validate(monkeypatch):
    monkeypatch.setattr(PyJWS, "__init__", lambda self: None)
    jws = PyJWS()
    headers = {"alg": "RS256"}
    jws._load = lambda jwt: (None, None, headers)

    def mock_validate(_):
        raise ValueError("invalid headers")

    jws._validate_headers = mock_validate

    with pytest.raises(ValueError):
        jws.get_unverified_header("token")

# short: ensures the function uses the headers object returned by _load
def test_get_unverified_header_uses_headers_from_load(monkeypatch):
    monkeypatch.setattr(PyJWS, "__init__", lambda self: None)
    jws = PyJWS()
    headers = {"kid": "abc", "alg": "none"}
    jws._load = lambda jwt: (None, None, headers)
    jws._validate_headers = lambda h: None

    result = jws.get_unverified_header("jwt32")

    assert result is headers
