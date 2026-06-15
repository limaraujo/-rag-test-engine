import pytest
from repositorios.pyjwt.jwt.exceptions import InvalidIssuedAtError, ImmatureSignatureError
from repositorios.pyjwt.jwt.api_jwt import PyJWT

# short: happy path - iat is numeric and within allowed window
def test_validate_iat_happy_path_no_exception():
    inst = PyJWT.__new__(PyJWT)
    payload = {"iat": "1000"}
    now = 1005
    leeway = 5
    assert inst._validate_iat(payload, now, leeway) is None

# short: invalid input - iat cannot be converted to int raises InvalidIssuedAtError
def test_validate_iat_invalid_issued_at_error_for_non_integer_input():
    inst = PyJWT.__new__(PyJWT)
    payload = {"iat": "notanint"}
    with pytest.raises(InvalidIssuedAtError):
        inst._validate_iat(payload, now=0.0, leeway=0.0)

# short: future iat beyond now+leeway raises ImmatureSignatureError
def test_validate_iat_immature_signature_error_when_iat_in_future():
    inst = PyJWT.__new__(PyJWT)
    payload = {"iat": "101"}
    with pytest.raises(ImmatureSignatureError):
        inst._validate_iat(payload, now=100, leeway=0)

# short: boundary case where iat equals now+leeway should not raise
def test_validate_iat_boundary_equal_now_plus_leeway_no_exception():
    inst = PyJWT.__new__(PyJWT)
    now = 50
    leeway = 10
    payload = {"iat": str(now + leeway)}
    assert inst._validate_iat(payload, now, leeway) is None
