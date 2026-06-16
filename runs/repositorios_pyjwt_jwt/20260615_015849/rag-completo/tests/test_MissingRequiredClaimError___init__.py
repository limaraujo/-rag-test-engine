from repositorios.pyjwt.jwt.exceptions import MissingRequiredClaimError

# happy path: verify attribute is set correctly for a typical claim
def test_missing_required_claim_init_sets_claim():
    err = MissingRequiredClaimError("iss")
    assert err.claim == "iss"

# edge case: verify behavior with an empty string as the claim
def test_missing_required_claim_init_with_empty_string_sets_claim():
    err = MissingRequiredClaimError("")
    assert err.claim == ""
