import pytest
from repositorios.pyjwt.jwt.api_jwt import PyJWT


# verifica TypeError ao usar audience de tipo inválido (caminho de exceção)
def test_invalid_audience_type_raises_type_error():
    jwt = PyJWT()
    payload = {"sub": "user"}
    options = {
        "require": [],
        "strict_aud": False,
        "verify_aud": False,
        "verify_exp": False,
        "verify_iat": False,
        "verify_iss": False,
        "verify_jti": False,
        "verify_nbf": False,
        "verify_sub": False,
        "enforce_minimum_key_length": False,
    }
    with pytest.raises(TypeError):
        jwt._validate_claims(payload, options, audience=123)


# verifica chamada de _validate_required_claims com payload e require (caso feliz)
def test_calls_validate_required_claims_with_payload_and_require():
    jwt = PyJWT()
    called = {}

    def fake_validate_required_claims(payload, require):
        called["payload"] = payload
        called["require"] = require

    jwt._validate_required_claims = fake_validate_required_claims

    payload = {"sub": "user"}
    options = {
        "require": ["sub"],
        "strict_aud": False,
        "verify_aud": False,
        "verify_exp": False,
        "verify_iat": False,
        "verify_iss": False,
        "verify_jti": False,
        "verify_nbf": False,
        "verify_sub": False,
        "enforce_minimum_key_length": False,
    }

    jwt._validate_claims(payload, options, audience=None, issuer=None, subject=None, leeway=0)

    assert called["payload"] == payload
    assert called["require"] == options["require"]


# verifica chamada de _validate_exp quando exp presente e verify_exp ativo (branch de exp)
def test_exp_claim_triggers_validate_exp_when_present():
    jwt = PyJWT()
    called = {}

    def fake_validate_exp(payload, now, leeway):
        called["payload"] = payload
        called["now"] = now
        called["leeway"] = leeway

    jwt._validate_exp = fake_validate_exp

    payload = {"exp": 9999999999}
    options = {
        "require": [],
        "strict_aud": False,
        "verify_aud": False,
        "verify_exp": True,
        "verify_iat": False,
        "verify_iss": False,
        "verify_jti": False,
        "verify_nbf": False,
        "verify_sub": False,
        "enforce_minimum_key_length": False,
    }

    jwt._validate_claims(payload, options, audience=None, issuer=None, subject=None, leeway=0)

    assert called["payload"] == payload
    assert isinstance(called["now"], (int, float))
    assert called["leeway"] == 0


# verifica chamada de _validate_aud com audience e strict quando verify_aud ativo
def test_aud_claim_calls_validate_aud_with_audience_and_strict():
    jwt = PyJWT()
    called = {}

    def fake_validate_aud(payload, audience, strict=False):
        called["payload"] = payload
        called["audience"] = audience
        called["strict"] = strict

    jwt._validate_aud = fake_validate_aud

    payload = {"aud": "aud1"}
    audience = "aud1"
    options = {
        "require": [],
        "strict_aud": True,
        "verify_aud": True,
        "verify_exp": False,
        "verify_iat": False,
        "verify_iss": False,
        "verify_jti": False,
        "verify_nbf": False,
        "verify_sub": False,
        "enforce_minimum_key_length": False,
    }

    jwt._validate_claims(payload, options, audience=audience, issuer=None, subject=None, leeway=0)

    assert called["payload"] == payload
    assert called["audience"] == audience
    assert called["strict"] is True
