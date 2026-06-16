import pytest
from repositorios.pyjwt.jwt.exceptions import MissingRequiredClaimError


# curto
def test_init_sets_claim():
    # happy path: __init__ stores the provided claim value
    obj = MissingRequiredClaimError("email")
    assert obj.claim == "email"

# curto
def test_init_accepts_non_string_claim():
    # edge case: __init__ accepts non-string claim values (type hint is not enforced at runtime)
    obj = MissingRequiredClaimError(123)
    assert obj.claim == 123

# curto
def test_str_uses_claim():
    # behavior dependent on __init__; verify __str__ uses stored claim
    obj = MissingRequiredClaimError("email")
    assert str(obj) == 'Token is missing the "email" claim'
