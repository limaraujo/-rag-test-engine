import pytest
from repositorios.pyjwt.jwt.api_jwt import PyJWT


class DummyPyJWT(PyJWT):
    def __init__(self):
        pass

    def decode_complete(self, jwt, key, algorithms, options, verify=None, detached_payload=None,
                        audience=None, subject=None, issuer=None, leeway=None, **kwargs):
        self.last_call = {
            "jwt": jwt,
            "key": key,
            "algorithms": algorithms,
            "options": options,
            "verify": verify,
            "detached_payload": detached_payload,
            "audience": audience,
            "subject": subject,
            "issuer": issuer,
            "leeway": leeway,
        }
        return {"payload": {"decoded": True}}

# Test 1: happy path - ensure decode delegates to decode_complete and returns payload
def test_decode_happy_path():
    jwt_obj = DummyPyJWT()
    result = jwt_obj.decode(
        "token",
        key="secret",
        algorithms=["HS256"],
        options={"verify_signature": True},
        audience="aud",
        subject="sub",
        issuer="iss",
        leeway=0,
    )
    assert result == {"decoded": True}
    assert jwt_obj.last_call["jwt"] == "token"
    assert jwt_obj.last_call["key"] == "secret"
    assert jwt_obj.last_call["algorithms"] == ["HS256"]

# Test 2: extra kwargs trigger warning and still call decode_complete
def test_decode_warns_on_extra_kwargs():
    jwt_obj = DummyPyJWT()
    with pytest.warns(Warning):
        result = jwt_obj.decode("token2", key="secret2", extra="value")
    assert result == {"decoded": True}
    assert jwt_obj.last_call["jwt"] == "token2"
    assert jwt_obj.last_call["key"] == "secret2"
