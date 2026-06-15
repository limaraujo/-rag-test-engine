import pytest
from repositorios.pyjwt.jwt.api_jwk import PyJWK



def _invoke_public_key_use(jwk: PyJWK):
    attr = getattr(jwk, "public_key_use")
    return attr() if callable(attr) else attr


@pytest.mark.parametrize("use_value", ["sig", "enc"])
def test_public_key_use_returns_value_when_present(use_value):
    jwk = PyJWK.__new__(PyJWK)
    jwk._jwk_data = {"use": use_value}
    assert _invoke_public_key_use(jwk) == use_value


def test_public_key_use_returns_none_when_missing():
    jwk = PyJWK.__new__(PyJWK)
    jwk._jwk_data = {}
    assert _invoke_public_key_use(jwk) is None


def test_public_key_use_returns_none_when_none_value():
    jwk = PyJWK.__new__(PyJWK)
    jwk._jwk_data = {"use": None}
    assert _invoke_public_key_use(jwk) is None
