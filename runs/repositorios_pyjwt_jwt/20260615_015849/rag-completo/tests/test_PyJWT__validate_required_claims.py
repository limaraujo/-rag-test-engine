import pytest
from repositorios.pyjwt.jwt.exceptions import MissingRequiredClaimError
from repositorios.pyjwt.jwt.api_jwt import PyJWT


def test_validate_required_claims_happy_path():
    instance = PyJWT.__new__(PyJWT)
    payload = {"sub": "user1", "aud": "aud1"}
    claims = ["sub", "aud"]
    instance._validate_required_claims(payload, claims)


def test_validate_required_claims_missing_claim_raises():
    instance = PyJWT.__new__(PyJWT)
    payload = {"sub": "user1"}
    claims = ["sub", "aud"]
    with pytest.raises(MissingRequiredClaimError) as excinfo:
        instance._validate_required_claims(payload, claims)
    assert excinfo.value.args[0] == "aud"


def test_validate_required_claims_none_value_raises():
    instance = PyJWT.__new__(PyJWT)
    payload = {"sub": None}
    claims = ["sub"]
    with pytest.raises(MissingRequiredClaimError) as excinfo:
        instance._validate_required_claims(payload, claims)
    assert excinfo.value.args[0] == "sub"
