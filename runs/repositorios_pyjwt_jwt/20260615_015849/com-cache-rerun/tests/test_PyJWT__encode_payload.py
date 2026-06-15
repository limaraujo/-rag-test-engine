import json
from repositorios.pyjwt.jwt.api_jwt import PyJWT

class DummyPyJWT(PyJWT):
    def __init__(self): 
        pass

# short: happy path - default encoding uses json.dumps with separators
def test_encode_payload_happy_path_default_encoding():
    payload = {"a": 1, "b": "two"}
    instance = DummyPyJWT()
    result = instance._encode_payload(payload)
    expected = json.dumps(payload, separators=(",", ":"), cls=None).encode("utf-8")
    assert result == expected

# short: encoder override - ensure provided json_encoder is used
def test_encode_payload_with_custom_encoder():
    class CustomObj:
        pass

    class CustomEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, CustomObj):
                return {"custom": True}
            return super().default(o)

    payload = {"a": CustomObj()}
    instance = DummyPyJWT()
    result = instance._encode_payload(payload, json_encoder=CustomEncoder)
    expected = json.dumps(payload, separators=(",", ":"), cls=CustomEncoder).encode("utf-8")
    assert result == expected

# short: headers parameter should not affect the encoded payload
def test_encode_payload_ignores_headers_argument():
    payload = {"a": 1}
    headers = {"kid": "abc"}
    instance = DummyPyJWT()
    with_headers = instance._encode_payload(payload, headers=headers)
    without_headers = instance._encode_payload(payload)
    assert with_headers == without_headers
