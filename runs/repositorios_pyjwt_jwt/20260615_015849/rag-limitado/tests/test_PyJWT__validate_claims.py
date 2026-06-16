import pytest
from datetime import timedelta
import time
from repositorios.pyjwt.jwt.api_jwt import PyJWT

class TestablePyJWT(PyJWT):
    def __init__(self, record):
        self._calls = record

    def _validate_required_claims(self, payload, require):
        self._calls["required"] = require

    def _validate_iat(self, payload, now, leeway):
        self._calls["iat"] = (now, leeway)

    def _validate_nbf(self, payload, now, leeway):
        self._calls["nbf"] = (now, leeway)

    def _validate_exp(self, payload, now, leeway):
        self._calls["exp"] = (now, leeway)

    def _validate_iss(self, payload, issuer):
        self._calls["iss"] = issuer

    def _validate_aud(self, payload, audience, strict=False):
        self._calls["aud"] = (audience, strict)

    def _validate_sub(self, payload, subject):
        self._calls["sub"] = subject

    def _validate_jti(self, payload):
        self._calls["jti"] = True

# Test 1: happy path - verify all validators are invoked with expected args
def test_validate_claims_happy_path_all_validators_called():
    # happy path: all relevant claims present and all verifications enabled
    calls = {}
    jwt = TestablePyJWT(calls)

    payload = {
        "iat": int(time.time()) - 5,
        "nbf": int(time.time()) - 10,
        "exp": int(time.time()) + 60,
    }

    options = {
        "require": ["exp", "nbf", "iss", "aud", "sub", "jti"],
        "verify_iat": True,
        "verify_nbf": True,
        "verify_exp": True,
        "verify_iss": True,
        "verify_aud": True,
        "verify_sub": True,
        "verify_jti": True,
        "strict_aud": False,
    }

    jwt._validate_claims(
        payload,
        options,
        audience="aud1",
        issuer="iss1",
        subject="sub1",
        leeway=timedelta(seconds=1),
    )

    assert calls.get("required") == options["require"]
    assert "iat" in calls
    assert "nbf" in calls
    assert "exp" in calls
    assert calls.get("iss") == "iss1"
    assert calls.get("aud") == ("aud1", False)
    assert calls.get("sub") == "sub1"
    assert calls.get("jti") is True

# Test 2: invalid audience type should raise TypeError
def test_validate_claims_invalid_audience_type_raises_typeerror():
    calls = {}
    jwt = TestablePyJWT(calls)

    payload = {"exp": int(time.time()) + 60}
    options = {
        "require": [],
        "verify_iat": False,
        "verify_nbf": False,
        "verify_exp": False,
        "verify_iss": False,
        "verify_aud": False,
        "verify_sub": False,
        "verify_jti": False,
        "strict_aud": False,
    }

    with pytest.raises(TypeError):
        jwt._validate_claims(payload, options, audience=123)

# Test 3: when verification flags are false, corresponding validators should not be called
def test_validate_claims_skip_validators_when_flags_false():
    calls = {}
    jwt = TestablePyJWT(calls)

    payload = {"iat": int(time.time()), "exp": int(time.time()) + 60}
    options = {
        "require": ["exp"],
        "verify_iat": False,
        "verify_nbf": False,
        "verify_exp": False,
        "verify_iss": False,
        "verify_aud": False,
        "verify_sub": False,
        "verify_jti": False,
        "strict_aud": False,
    }

    jwt._validate_claims(payload, options, audience=None, issuer=None, subject=None, leeway=0)

    assert "iat" not in calls
    assert "exp" not in calls
    assert calls.get("required") == options["require"]
