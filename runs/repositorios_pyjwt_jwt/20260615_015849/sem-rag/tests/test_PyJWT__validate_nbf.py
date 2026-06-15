import pytest
from repositorios.pyjwt.jwt.exceptions import DecodeError, ImmatureSignatureError
from repositorios.pyjwt.jwt.api_jwt import PyJWT

# helper to instantiate PyJWT without running __init__
def _new_pyjwt():
    return PyJWT.__new__(PyJWT)

# short: happy path - nbf within allowed window should not raise

def test_nbf_happy_path_no_exception():
    # happy path: nbf <= now + leeway
    token = _new_pyjwt()
    now = 1000.0
    leeway = 0.0
    payload = {"nbf": int(now) - 1}
    token._validate_nbf(payload, now, leeway)

# short: branch - token not yet valid should raise ImmatureSignatureError

def test_nbf_immature_signature_raises():
    # branch: nbf > now + leeway triggers ImmatureSignatureError
    token = _new_pyjwt()
    now = 1000.0
    leeway = 0.0
    payload = {"nbf": int(now) + 1}
    with pytest.raises(ImmatureSignatureError) as exc:
        token._validate_nbf(payload, now, leeway)
    assert "not yet valid" in str(exc.value)

# short: branch - non-integer nbf should raise DecodeError

def test_nbf_non_integer_raises_decode_error():
    # edge: invalid input for nbf causes DecodeError
    token = _new_pyjwt()
    now = 1000.0
    leeway = 0.0
    payload = {"nbf": "abc"}
    with pytest.raises(DecodeError) as exc:
        token._validate_nbf(payload, now, leeway)
    assert "Not Before claim (nbf) must be an integer." in str(exc.value)

# short: border case - missing 'nbf' key raises KeyError (invalid input)

def test_nbf_missing_key_raises_key_error():
    # border: invalid_input when 'nbf' key is absent
    token = _new_pyjwt()
    now = 1000.0
    leeway = 0.0
    payload = {}
    with pytest.raises(KeyError):
        token._validate_nbf(payload, now, leeway)
