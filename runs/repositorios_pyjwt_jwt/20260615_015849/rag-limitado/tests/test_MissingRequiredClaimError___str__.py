import pytest
from repositorios.pyjwt.jwt.exceptions import MissingRequiredClaimError

# Verifica que __str__ retorna a mensagem esperada para diferentes claims (caso feliz)
@pytest.mark.parametrize("claim, expected", [
    ("sub", 'Token is missing the "sub" claim'),
    ("aud", 'Token is missing the "aud" claim'),
    ("", 'Token is missing the "" claim'),
])
def test_missing_required_claim_str(claim, expected):
    exc = MissingRequiredClaimError(claim)
    assert str(exc) == expected
