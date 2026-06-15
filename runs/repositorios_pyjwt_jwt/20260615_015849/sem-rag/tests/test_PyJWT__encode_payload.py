import json
from repositorios.pyjwt.jwt.api_jwt import PyJWT

# short: happy path - encode simple payload to bytes without custom encoder
def test_encode_payload_happy_path_basic():
    obj = PyJWT.__new__(PyJWT)
    payload = {"foo": 1, "bar": "baz"}
    expected = json.dumps(payload, separators=(",", ":"), cls=None).encode("utf-8")
    assert PyJWT._encode_payload(obj, payload) == expected

# short: uses a provided json_encoder to handle non-JSON-serializable types (e.g., set)
def test_encode_payload_with_custom_json_encoder():
    class _SetEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, set):
                return sorted(o)
            return super().default(o)

    obj = PyJWT.__new__(PyJWT)
    payload = {"s": {3, 2, 1}}
    expected = json.dumps(payload, separators=(",", ":"), cls=_SetEncoder).encode("utf-8")
    actual = PyJWT._encode_payload(obj, payload, json_encoder=_SetEncoder)
    assert actual == expected

# short: headers argument should be ignored by this base implementation
def test_encode_payload_ignores_headers_argument():
    obj = PyJWT.__new__(PyJWT)
    payload = {"a": 1}
    headers = {"kid": "abc"}
    expected = json.dumps(payload, separators=(",", ":"), cls=None).encode("utf-8")
    actual = PyJWT._encode_payload(obj, payload, headers=headers)
    assert actual == expected

# short: empty payload encodes to {}
def test_encode_payload_empty_payload():
    obj = PyJWT.__new__(PyJWT)
    payload = {}
    expected = json.dumps(payload, separators=(",", ":"), cls=None).encode("utf-8")
    actual = PyJWT._encode_payload(obj, payload)
    assert actual == expected
