import pytest
from repositorios.pyjwt.jwt.exceptions import MissingRequiredClaimError
from repositorios.pyjwt.jwt.api_jwt import PyJWT

# happy path: all required claims are present, no exception raised
def test_happy_path_single_claims_list_no_exception():
    jwt = PyJWT()
    payload = {'sub': 'user', 'aud': 'aud1'}
    claims = ['sub', 'aud']
    jwt._validate_required_claims(payload, claims)

# missing required claim raises MissingRequiredClaimError
def test_missing_claim_raises_error():
    jwt = PyJWT()
    payload = {'sub': 'user'}
    claims = ['sub', 'aud']
    with pytest.raises(MissingRequiredClaimError) as exc:
        jwt._validate_required_claims(payload, claims)
    assert exc.value.args[0] == 'aud'

# None value for a required claim should raise MissingRequiredClaimError
def test_none_value_raises_error():
    jwt = PyJWT()
    payload = {'sub': None}
    claims = ['sub']
    with pytest.raises(MissingRequiredClaimError) as exc:
        jwt._validate_required_claims(payload, claims)
    assert exc.value.args[0] == 'sub'

# various iterable types for claims should work (happy path)
@pytest.mark.parametrize("claims_iterable", [
    ['a', 'b'],
    ('a', 'b'),
    {'a', 'b'},
])
def test_happy_path_various_iterables_no_exception(claims_iterable):
    jwt = PyJWT()
    payload = {'a': 1, 'b': 2}
    jwt._validate_required_claims(payload, claims_iterable)
