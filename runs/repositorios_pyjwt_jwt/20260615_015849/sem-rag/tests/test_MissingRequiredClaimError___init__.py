import pytest
from repositorios.pyjwt.jwt.exceptions import MissingRequiredClaimError


# Verifica que __init__ armazena o claim fornecido para diferentes valores (casos: string simples, string vazia, string longa)
@pytest.mark.parametrize("input_claim", ["email", "", "username_required"])
def test_missing_required_claim_error_init_sets_claim(input_claim):
    exc = MissingRequiredClaimError(input_claim)
    assert exc.claim == input_claim
