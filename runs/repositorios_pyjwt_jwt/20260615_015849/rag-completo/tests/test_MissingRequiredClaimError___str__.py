import pytest
from repositorios.pyjwt.jwt.exceptions import MissingRequiredClaimError

# happy path: __str__ inclui a claim fornecida
@pytest.mark.parametrize("claim", ["email", "token id", "¡nombre!"])
def test_missing_required_claim_str_includes_claim(claim):
    err = MissingRequiredClaimError(claim)
    assert str(err) == f'Token is missing the "{claim}" claim'
