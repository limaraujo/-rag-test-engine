import pytest
from repositorios.pyjwt.jwt.api_jwt import PyJWT


def _make_jwt_instance() -> PyJWT:
    return object.__new__(PyJWT)

# happy path: iat within allowed window (no exception)
def test_validate_iat_happy_path_no_exception():
    jwt = _make_jwt_instance()
    now = 1000.0
    leeway = 10.0
    payload = {"iat": int(now)}  # iat == now, within window
    jwt._validate_iat(payload, now, leeway)

# invalid input: iat cannot be parsed as int -> InvalidIssuedAtError
def test_validate_iat_invalid_input_raises_InvalidIssuedAtError():
    jwt = _make_jwt_instance()
    now = 1000.0
    leeway = 10.0
    payload = {"iat": "notanint"}
    with pytest.raises(Exception) as exc:
        jwt._validate_iat(payload, now, leeway)
    assert exc.value.__class__.__name__ == "InvalidIssuedAtError"

# future iat beyond allowed window -> ImmatureSignatureError
def test_validate_iat_future_immature_signature_error():
    jwt = _make_jwt_instance()
    now = 1000.0
    leeway = 10.0
    payload = {"iat": int(now + leeway) + 1}
    with pytest.raises(Exception) as exc:
        jwt._validate_iat(payload, now, leeway)
    assert exc.value.__class__.__name__ == "ImmatureSignatureError"
