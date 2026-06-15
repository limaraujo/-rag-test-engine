import pytest
from repositorios.pyjwt.jwt.exceptions import MissingRequiredClaimError

# happy path: valida saída para várias claims
@pytest.mark.parametrize("claim", ["aud", "iss", "sub"])
def test_missing_required_claim_str_happy_path_parametrized(claim):
    e = MissingRequiredClaimError(claim)
    assert str(e) == f'Token is missing the "{claim}" claim'

# edge: claim com aspas internas para garantir formatação
def test_missing_required_claim_str_handles_quotes_in_claim():
    claim = 'a"b'
    e = MissingRequiredClaimError(claim)
    assert str(e) == f'Token is missing the "{claim}" claim'
