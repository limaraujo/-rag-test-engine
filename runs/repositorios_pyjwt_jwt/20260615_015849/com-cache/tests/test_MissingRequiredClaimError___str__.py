import pytest
from repositorios.pyjwt.jwt.exceptions import MissingRequiredClaimError

# curto: verifica __str__ retorna formato esperado para diferentes claims (caso happy path)
@pytest.mark.parametrize("claim", ["exp", "nbf", "custom_claim", 'a"b'])
def test_missing_required_claim_error_str_includes_claim(claim):
    err = MissingRequiredClaimError(claim)
    assert str(err) == f'Token is missing the "{claim}" claim'
