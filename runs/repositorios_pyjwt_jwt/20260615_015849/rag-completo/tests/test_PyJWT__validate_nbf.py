import pytest
from repositorios.pyjwt.jwt.exceptions import DecodeError, ImmatureSignatureError
from repositorios.pyjwt.jwt.api_jwt import PyJWT

def _make_instance():
    return object.__new__(PyJWT)

# happy path: nbf <= now+leeway should not raise
def test_validate_nbf_happy_path():
    obj = _make_instance()
    now = 1000.0
    leeway = 5.0
    payload = {"nbf": int(now - 1)}
    PyJWT._validate_nbf(obj, payload, now, leeway)

# invalid input: non-integer nbf should raise DecodeError
def test_validate_nbf_invalid_input_raises_decodeerror():
    obj = _make_instance()
    now = 0.0
    leeway = 0.0
    payload = {"nbf": "notanint"}
    with pytest.raises(DecodeError):
        PyJWT._validate_nbf(obj, payload, now, leeway)

# future nbf: nbf > now+leeway should raise ImmatureSignatureError
def test_validate_nbf_future_raises_immaturesignatureerror():
    obj = _make_instance()
    now = 100.0
    leeway = 0.0
    payload = {"nbf": 200}
    with pytest.raises(ImmatureSignatureError):
        PyJWT._validate_nbf(obj, payload, now, leeway)
