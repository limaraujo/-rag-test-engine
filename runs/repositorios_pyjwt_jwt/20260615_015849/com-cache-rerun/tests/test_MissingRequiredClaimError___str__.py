import pytest
from repositorios.pyjwt.jwt.exceptions import MissingRequiredClaimError

# curto: happy path; __init__ deve atribuir a claim fornecida ao atributo 'claim'
def test_missing_required_claim_error_init_sets_claim():
    claim = "exp"
    err = MissingRequiredClaimError(claim)
    assert err.claim == claim

# curto: happy path; __str__ deve retornar a string formatada corretamente para claim simples
def test_missing_required_claim_error_str_happy_path():
    claim = "exp"
    err = MissingRequiredClaimError(claim)
    assert str(err) == 'Token is missing the "exp" claim'

# curto: casos de borda/cotidiano; valida __str__ com claims incluindo aspas no conteúdo
@pytest.mark.parametrize("claim", ["exp", "nbf", "custom_claim", 'a"b'])
def test_missing_required_claim_error_str_parametrized(claim):
    err = MissingRequiredClaimError(claim)
    assert str(err) == f'Token is missing the "{claim}" claim'
