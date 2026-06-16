import pytest
from repositorios.pyjwt.jwt.exceptions import InvalidAudienceError, MissingRequiredClaimError
from repositorios.pyjwt.jwt.api_jwt import PyJWT

# curto
# teste de caminho feliz: sem audience (None) e payload sem claim 'aud' -> não lança
def test_validate_aud_none_no_aud_in_payload_returns_none():
    inst = PyJWT.__new__(PyJWT)
    payload = {}
    PyJWT._validate_aud(inst, payload, None, strict=False)

# curto
# verifica exceção quando audience é None mas payload possui 'aud' -> InvalidAudienceError
def test_validate_aud_none_with_aud_in_payload_raises_InvalidAudienceError():
    inst = PyJWT.__new__(PyJWT)
    payload = {"aud": "foo"}
    with pytest.raises(InvalidAudienceError):
        PyJWT._validate_aud(inst, payload, None, strict=False)

# curto
# falta de claim obrigatória 'aud' quando audience é fornecido -> MissingRequiredClaimError
def test_validate_aud_missing_claim_when_audience_provided_raises_MissingRequiredClaimError():
    inst = PyJWT.__new__(PyJWT)
    payload = {}
    with pytest.raises(MissingRequiredClaimError):
        PyJWT._validate_aud(inst, payload, "foo", strict=False)

# longo
# cenários combinados (strict e não-strict) em uma única parametrização para cobrir várias ramificações
@pytest.mark.parametrize("case", [
    # strict: match exata
    {"description": "strict match passes", "audience": "aud1", "payload": {"aud": "aud1"}, "strict": True, "should_raise": False},
    # strict: audiência fornecida não é string
    {"description": "strict invalid audience type", "audience": ["aud1"], "payload": {"aud": "aud1"}, "strict": True, "should_raise": True, "exception": InvalidAudienceError},
    # strict: claim de token não é string
    {"description": "strict invalid claim format in token", "audience": "aud1", "payload": {"aud": ["aud1"]}, "strict": True, "should_raise": True, "exception": InvalidAudienceError},
    # strict: mismatch
    {"description": "strict mismatch", "audience": "aud2", "payload": {"aud": "aud1"}, "strict": True, "should_raise": True, "exception": InvalidAudienceError},
    # não-strict: único 'aud' igual
    {"description": "non-strict single string matches", "audience": "aud1", "payload": {"aud": "aud1"}, "strict": False, "should_raise": False},
    # não-strict: múltiplos claims onde pelo menos um bate
    {"description": "non-strict multiple claims with match", "audience": ["aud1", "aud3"], "payload": {"aud": ["aud2", "aud1"]}, "strict": False, "should_raise": False},
    # não-strict: nenhum match
    {"description": "non-strict no match raises", "audience": "aud4", "payload": {"aud": ["aud1", "aud2"]}, "strict": False, "should_raise": True, "exception": InvalidAudienceError},
])
def test_validate_aud_parametrized_case(case):
    inst = PyJWT.__new__(PyJWT)
    payload = case["payload"]
    audience = case["audience"]
    strict = case["strict"]
    if case["should_raise"]:
        with pytest.raises(case.get("exception", InvalidAudienceError)):
            PyJWT._validate_aud(inst, payload, audience, strict=strict)
    else:
        PyJWT._validate_aud(inst, payload, audience, strict=strict)
