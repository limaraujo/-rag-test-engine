import pytest
from repositorios.pyjwt.jwt.api_jws import PyJWS

# curto: happy path sem kwargs
def test_decode_no_kwargs_returns_payload():
    class DummyPyJWS(PyJWS):
        def __init__(self):
            pass

        def decode_complete(self, jwt, key, algorithms, options, detached_payload=None):
            self.called_with = {
                "jwt": jwt,
                "key": key,
                "algorithms": algorithms,
                "options": options,
                "detached_payload": detached_payload,
            }
            return {"payload": "decoded_payload"}

    dj = DummyPyJWS()
    result = dj.decode("jwt_string", key="my_key", algorithms=["HS256"], options=None, detached_payload=b"detached")
    assert result == "decoded_payload"
    assert dj.called_with == {
        "jwt": "jwt_string",
        "key": "my_key",
        "algorithms": ["HS256"],
        "options": None,
        "detached_payload": b"detached",
    }

# curto: path com kwargs gera warning RemovedInPyjwt3Warning e retorna payload
def test_decode_with_kwargs_emits_warning_and_returns_payload():
    class DummyPyJWS(PyJWS):
        def __init__(self):
            pass

        def decode_complete(self, jwt, key, algorithms, options, detached_payload=None):
            self.called_with = {
                "jwt": jwt,
                "key": key,
                "algorithms": algorithms,
                "options": options,
                "detached_payload": detached_payload,
            }
            return {"payload": "decoded_payload"}

    dj = DummyPyJWS()
    with pytest.warns(Warning) as record:
        result = dj.decode("jwt_with_kw", key="K", algorithms=None, options=None, detached_payload=None, extra_param=123)

    assert result == "decoded_payload"
    assert dj.called_with == {
        "jwt": "jwt_with_kw",
        "key": "K",
        "algorithms": None,
        "options": None,
        "detached_payload": None,
    }
    assert len(record) == 1
