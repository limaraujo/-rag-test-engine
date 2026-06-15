import pytest
from repositorios.pyjwt.jwt.exceptions import DecodeError, ImmatureSignatureError
from repositorios.pyjwt.jwt.api_jwt import PyJWT

# happy path: nbf is not greater than now + leeway
def test_happy_path_nbf_within_allowed_window():
    obj = PyJWT.__new__(PyJWT)
    payload = {"nbf": 100}
    now = 100
    leeway = 5
    # should not raise
    obj._validate_nbf(payload, now, leeway)

# invalid input: nbf not an integer convertible value triggers DecodeError
def test_invalid_input_raises_DecodeError_for_nbf():
    obj = PyJWT.__new__(PyJWT)
    payload = {"nbf": "notanint"}
    with pytest.raises(DecodeError) as exc:
        obj._validate_nbf(payload, now=0, leeway=0)
    assert "Not Before claim (nbf) must be an integer." in str(exc.value)

# future time: nbf greater than now + leeway raises ImmatureSignatureError
def test_future_nbf_raises_ImmatureSignatureError():
    obj = PyJWT.__new__(PyJWT)
    payload = {"nbf": 10}
    now = 5
    leeway = 0
    with pytest.raises(ImmatureSignatureError):
        obj._validate_nbf(payload, now, leeway)
