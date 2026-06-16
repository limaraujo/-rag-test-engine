from repositorios.pyjwt.jwt.exceptions import DecodeError
import json
import pytest
from repositorios.pyjwt.jwt.api_jwt import PyJWT

# happy path: valid JSON payload decodes to a Python dict
def test_decode_payload_happy_path():
    pyjwt = PyJWT.__new__(PyJWT)
    payload = {"user": "alice", "role": "admin"}
    decoded = {"payload": json.dumps(payload)}
    assert pyjwt._decode_payload(decoded) == payload

# error: invalid payload string should raise DecodeError with informative message
def test_decode_payload_invalid_json_raises_decode_error():
    pyjwt = PyJWT.__new__(PyJWT)
    decoded = {"payload": "not a valid json"}
    with pytest.raises(DecodeError) as excinfo:
        pyjwt._decode_payload(decoded)
    assert "Invalid payload string" in str(excinfo.value)

# error: payload JSON loads to non-dict should raise DecodeError
def test_decode_payload_json_not_object_raises_decode_error():
    pyjwt = PyJWT.__new__(PyJWT)
    decoded = {"payload": json.dumps([1, 2, 3])}
    with pytest.raises(DecodeError) as excinfo:
        pyjwt._decode_payload(decoded)
    assert "must be a json object" in str(excinfo.value)
