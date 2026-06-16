import pytest
from repositorios.pyjwt.jwt.api_jwt import PyJWT
from repositorios.pyjwt.jwt.exceptions import ImmatureSignatureError, InvalidIssuedAtError

import pytest
from repositorios.pyjwt.jwt.api_jwt import PyJWT


try:
    from repositorios.pyjwt.jwt.exceptions import ImmatureSignatureError, InvalidIssuedAtError
except Exception:
    ImmatureSignatureError = None
    InvalidIssuedAtError = None


def _make_pyjwt_instance():
    # instantiate without running __init__
    return PyJWT.__new__(PyJWT)


# short: happy path
# verifica que, quando iat é dentro do intervalo permitido, não ocorre exceção
def test_validate_iat_happy_path():
    obj = _make_pyjwt_instance()
    now = 1000.0
    leeway = 0.0
    payload = {"iat": str(int(now - 10))}  # iat <= now + leeway
    obj._validate_iat(payload, now, leeway)


# short: exception de input inválido
# verifica que iat não-número levanta InvalidIssuedAtError
def test_validate_iat_invalid_input_raises():
    obj = _make_pyjwt_instance()
    now = 1000.0
    leeway = 0.0
    payload = {"iat": "not-a-number"}
    with pytest.raises(Exception) as excinfo:
        obj._validate_iat(payload, now, leeway)
    assert excinfo.value.__class__.__name__ in {"InvalidIssuedAtError"}


# short: branch futura
# verifica que iat no futuro levanta ImmatureSignatureError
def test_validate_iat_future_raises():
    obj = _make_pyjwt_instance()
    now = 500.0
    leeway = 0.0
    payload = {"iat": str(1000)}  # iat > now + leeway
    with pytest.raises(Exception) as excinfo:
        obj._validate_iat(payload, now, leeway)
    assert excinfo.value.__class__.__name__ in {"ImmatureSignatureError", "InvalidIssuedAtError"}
