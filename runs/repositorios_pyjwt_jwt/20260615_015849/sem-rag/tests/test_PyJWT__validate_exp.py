import pytest
from repositorios.pyjwt.jwt.exceptions import DecodeError, ExpiredSignatureError
from repositorios.pyjwt.jwt.api_jwt import PyJWT

def test_validate_exp_happy_path_no_exception():
    jwt = PyJWT()
    payload = {"exp": 1003}
    # now - leeway = 995; 1003 > 995 -> no exception
    jwt._validate_exp(payload, now=1000, leeway=5)

def test_validate_exp_decode_error_on_non_integer_exp():
    jwt = PyJWT()
    payload = {"exp": "not-an-integer"}
    with pytest.raises(DecodeError) as exc:
        jwt._validate_exp(payload, now=1000, leeway=0)
    assert "Expiration Time claim (exp) must be an integer." in str(exc.value)

@pytest.mark.parametrize("exp,now,leeway", [
    (990, 1000, 10),  # equal to the boundary: exp <= now - leeway
    (989, 1000, 10),  # below the boundary
])
def test_validate_exp_expired_on_or_before_boundary(exp, now, leeway):
    jwt = PyJWT()
    with pytest.raises(ExpiredSignatureError):
        jwt._validate_exp({"exp": exp}, now=now, leeway=leeway)
