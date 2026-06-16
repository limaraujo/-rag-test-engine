import pytest
from repositorios.pyjwt.jwt.exceptions import MissingRequiredClaimError
from repositorios.pyjwt.jwt.api_jwt import PyJWT

# happy path: nenhum claim ausente no payload
def test__validate_required_claims_happy_path():
    obj = PyJWT.__new__(PyJWT)
    payload = {"iss": "issuer", "sub": "subject"}
    claims = ["iss", "sub"]
    PyJWT._validate_required_claims(obj, payload, claims)

# exception path: claim obrigatório ausente deve levantar MissingRequiredClaimError
def test__validate_required_claims_missing_claim_raises():
    obj = PyJWT.__new__(PyJWT)
    payload = {"iss": "issuer"}  # falta "sub"
    claims = ["iss", "sub"]
    with pytest.raises(MissingRequiredClaimError) as exc:
        PyJWT._validate_required_claims(obj, payload, claims)
    assert exc.value.args[0] == "sub"
