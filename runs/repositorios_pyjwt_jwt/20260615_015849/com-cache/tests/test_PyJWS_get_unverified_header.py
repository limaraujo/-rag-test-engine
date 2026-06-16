import pytest
from repositorios.pyjwt.jwt.api_jws import PyJWS

# Subclass to bypass heavy __init__ of PyJWS for isolated unit testing
class _TestPyJWS(PyJWS):
    def __init__(self):
        pass

# Test: happy path - returns unverified header and calls _load/_validate_headers
def test_get_unverified_header_happy_path():
    # short: happy path
    inst = _TestPyJWS()
    expected_headers = {"typ": "JWT", "alg": "HS256"}
    captured = {}

    def fake_load(jwt):
        captured["jwt"] = jwt
        return (None, None, expected_headers)

    def fake_validate(headers):
        captured["validated"] = headers

    inst._load = fake_load
    inst._validate_headers = fake_validate

    result = inst.get_unverified_header("header.jwt")

    assert result == expected_headers
    assert captured["jwt"] == "header.jwt"
    assert captured["validated"] == expected_headers

# Test: exception from _validate_headers propagates
def test_get_unverified_header_propagates_validation_exception():
    # short: exception propagation
    inst = _TestPyJWS()
    headers = {"typ": "JWT"}
    inst._load = lambda jwt: (None, None, headers)

    def fake_validate(headers):
        raise ValueError("invalid headers")

    inst._validate_headers = fake_validate

    with pytest.raises(ValueError):
        inst.get_unverified_header("token")

# Test: ensure bytes input is passed to _load unchanged
def test_get_unverified_header_passes_bytes_input():
    # short: input as bytes
    inst = _TestPyJWS()
    headers = {"a": 1}
    captured = {}

    def fake_load(jwt):
        captured["jwt"] = jwt
        return (None, None, headers)

    inst._load = fake_load
    inst._validate_headers = lambda h: None

    _ = inst.get_unverified_header(b"byte.jwt")

    assert captured["jwt"] == b"byte.jwt"

# Test: ensure string input is passed to _load unchanged
def test_get_unverified_header_passes_str_input():
    # short: input as string
    inst = _TestPyJWS()
    headers = {"a": 2}
    captured = {}

    def fake_load(jwt):
        captured["jwt"] = jwt
        return (None, None, headers)

    inst._load = fake_load
    inst._validate_headers = lambda h: None

    _ = inst.get_unverified_header("string.jwt")

    assert captured["jwt"] == "string.jwt"
