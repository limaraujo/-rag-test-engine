from repositorios.pyjwt.jwt.exceptions import MissingRequiredClaimError

# curto: happy path; __init__ deve atribuir a claim fornecida ao atributo 'claim'
def test_missing_required_claim_error_init_sets_claim():
    claim = "exp"
    err = MissingRequiredClaimError(claim)
    assert isinstance(err, MissingRequiredClaimError)
    assert err.claim == claim
