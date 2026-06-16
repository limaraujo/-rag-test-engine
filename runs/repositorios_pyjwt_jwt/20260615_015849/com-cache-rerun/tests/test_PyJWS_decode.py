import pytest
from repositorios.pyjwt.jwt.api_jws import PyJWS


# verifica o caminho feliz: decode retorna o payload obtido de decode_complete
def test_pyjws_decode_happy_path_returns_payload_and_calls_decode_complete():
    class DummyPyJWS(PyJWS):
        def __init__(self):
            pass

        def decode_complete(self, jwt, key, algorithms=None, options=None, detached_payload=None, **kwargs):
            self.captured = {
                "jwt": jwt,
                "key": key,
                "algorithms": algorithms,
                "options": options,
                "detached_payload": detached_payload,
            }
            return {"payload": {"user": "alice"}}

    obj = DummyPyJWS()
    payload = obj.decode(
        "jwt_str",
        key="mykey",
        algorithms=["HS256"],
        options={"a": 1},
        detached_payload=b"detached",
    )

    assert payload == {"user": "alice"}
    assert obj.captured == {
        "jwt": "jwt_str",
        "key": "mykey",
        "algorithms": ["HS256"],
        "options": {"a": 1},
        "detached_payload": b"detached",
    }


# verifica que kwargs adicionais geram warning de deprecação
def test_pyjws_decode_warns_on_extra_kwargs():
    class DummyPyJWS(PyJWS):
        def __init__(self):
            pass

        def decode_complete(self, jwt, key, algorithms=None, options=None, detached_payload=None, **kwargs):
            self.captured = True
            return {"payload": {"ok": True}}

    obj = DummyPyJWS()
    with pytest.warns(Warning):
        result = obj.decode("jwt_with_kwargs", extra="value")

    assert result == {"ok": True}
