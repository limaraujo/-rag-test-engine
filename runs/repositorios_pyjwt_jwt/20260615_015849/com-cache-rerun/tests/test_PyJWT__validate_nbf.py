import pytest
from repositorios.pyjwt.jwt.api_jwt import PyJWT
from repositorios.pyjwt.jwt.exceptions import DecodeError, ImmatureSignatureError

import pytest
from repositorios.pyjwt.jwt.api_jwt import PyJWT


try:
    from repositorios.pyjwt.jwt.exceptions import DecodeError, ImmatureSignatureError
except Exception:
    DecodeError = None
    ImmatureSignatureError = None

# short: invalid nbf input should raise DecodeError
def test__validate_nbf_raises_decode_error_on_invalid_input():
    # invalid_input: nbf cannot be parsed as int
    obj = PyJWT.__new__(PyJWT)
    payload = {"nbf": "not-an-int"}
    now = 1000.0
    leeway = 0.0
    expected = DecodeError if DecodeError is not None else Exception
    with pytest.raises(expected):
        obj._validate_nbf(payload, now, leeway)

# short: nbf in the future should raise ImmatureSignatureError
def test__validate_nbf_raises_immature_when_nbf_in_future():
    # future nbf: nbf > now + leeway
    obj = PyJWT.__new__(PyJWT)
    payload = {"nbf": 1001}
    now = 1000.0
    leeway = 0.0
    expected = ImmatureSignatureError if ImmatureSignatureError is not None else Exception
    with pytest.raises(expected):
        obj._validate_nbf(payload, now, leeway)

# short: boundary case where nbf equals now + leeway should not raise
def test__validate_nbf_passes_when_nbf_is_on_boundary():
    # boundary: nbf == now + leeway
    obj = PyJWT.__new__(PyJWT)
    payload = {"nbf": 10}
    now = 10.0
    leeway = 0.0
    # should not raise
    obj._validate_nbf(payload, now, leeway)

# short: string numeric nbf within range should not raise
def test__validate_nbf_accepts_string_numeric_and_passes():
    obj = PyJWT.__new__(PyJWT)
    payload = {"nbf": "5"}  # string numeric
    now = 10.0
    leeway = 0.0
    obj._validate_nbf(payload, now, leeway)
