import pytest
from repositorios.pyjwt.jwt.exceptions import InvalidAudienceError, MissingRequiredClaimError
from repositorios.pyjwt.jwt.api_jwt import PyJWT

import pytest

from repositorios.pyjwt.jwt.exceptions import InvalidAudienceError, MissingRequiredClaimError
from repositorios.pyjwt.jwt.api_jwt import PyJWT

# verifica o caminho happy path: nenhum aud é fornecido e o payload não possui 'aud'
def test_validate_aud_none_no_aud_provided_happy_path():
    payload = {"sub": "user123"}
    PyJWT._validate_aud(object(), payload, None)

# verifica exceção quando audience é None mas o token tem a claim 'aud'
def test_validate_aud_none_with_aud_raises_invalid_audience():
    payload = {"aud": "token_aud"}
    with pytest.raises(InvalidAudienceError):
        PyJWT._validate_aud(object(), payload, None)

# verifica MissingRequiredClaimError quando audience é fornecido mas a claim aud está ausente
def test_validate_aud_requires_aud_claim_if_audience_provided():
    payload = {"sub": "user123"}
    with pytest.raises(MissingRequiredClaimError):
        PyJWT._validate_aud(object(), payload, "expected_audience")

# verifica strict mode com cenários variados (not string audience, non-string claim, match, mismatch)
@pytest.mark.parametrize("scenario", [
    {"audience": ["a"], "payload_aud": "a", "should_raise": InvalidAudienceError},
    {"audience": "a", "payload_aud": ["a"], "should_raise": InvalidAudienceError},
    {"audience": "a", "payload_aud": "a", "should_raise": None},
    {"audience": "a", "payload_aud": "b", "should_raise": InvalidAudienceError},
])
def test_validate_aud_strict_mode_various_scenarios(scenario):
    audience = scenario["audience"]
    payload_aud = scenario["payload_aud"]
    should_raise = scenario["should_raise"]

    payload = {"aud": payload_aud} if payload_aud is not None else {}

    if should_raise is None:
        PyJWT._validate_aud(object(), payload, audience, strict=True)
    else:
        with pytest.raises(should_raise):
            PyJWT._validate_aud(object(), payload, audience, strict=True)
