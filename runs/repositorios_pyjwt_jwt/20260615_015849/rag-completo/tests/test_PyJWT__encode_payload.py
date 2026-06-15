import json
import pytest
from repositorios.pyjwt.jwt.api_jwt import PyJWT


# short
class DummyPyJWT(PyJWT):
    def __init__(self):  # avoid complex initialization in tests
        pass


# short
def test_encode_payload_basic_no_encoder():
    # happy path: simple payload with default encoder
    jwt = DummyPyJWT()
    payload = {"a": 1, "b": "x"}
    expected = json.dumps(payload, separators=(",", ":"), cls=None).encode("utf-8")
    assert jwt._encode_payload(payload) == expected


# short
def test_encode_payload_with_custom_encoder():
    # branch: custom json_encoder handles non-default serialization (e.g., set)
    jwt = DummyPyJWT()
    payload = {"a": {1, 2, 3}}

    class SetEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, set):
                return sorted(list(o))
            return super().default(o)

    expected = json.dumps(payload, separators=(",", ":"), cls=SetEncoder).encode("utf-8")
    assert jwt._encode_payload(payload, json_encoder=SetEncoder) == expected


# short
def test_encode_payload_ignores_headers():
    # branch: headers argument is ignored by implementation
    jwt = DummyPyJWT()
    payload = {"a": 1}
    headers = {"alg": "HS256", "typ": "JWT"}
    expected = json.dumps(payload, separators=(",", ":"), cls=None).encode("utf-8")
    assert jwt._encode_payload(payload, headers=headers) == expected


# short
def test_encode_payload_raises_type_error_on_unserializable():
    # exception: non-serializable payload without encoder
    jwt = DummyPyJWT()
    class NonSerializable:
        pass
    payload = {"a": NonSerializable()}
    with pytest.raises(TypeError):
        jwt._encode_payload(payload)
