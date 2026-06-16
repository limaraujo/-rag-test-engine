import json
import base64
import pytest
from repositorios.pyjwt.jwt.exceptions import DecodeError
from repositorios.pyjwt.jwt.api_jws import PyJWS

import json
import base64
import pytest

from repositorios.pyjwt.jwt.exceptions import DecodeError
from repositorios.pyjwt.jwt.api_jws import PyJWS

# Helper to create a base64url-encoded string from bytes
def _b64url(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).decode("ascii").rstrip("=")

# Initialize PyJWS instance without invoking __init__
def _make_instance():
    return PyJWS.__new__(PyJWS)

# short: happy path - valid token returns decoded payload, header, and signature
def test_load_happy_path():
    header = {"alg": "HS256"}
    header_json = json.dumps(header).encode("utf-8")
    header_b64 = _b64url(header_json)

    payload_bytes = b"payloadbytes"
    payload_b64 = _b64url(payload_bytes)

    signature_bytes = b"signaturebytes"
    signature_b64 = _b64url(signature_bytes)

    jwt_token = (header_b64 + "." + payload_b64 + "." + signature_b64).encode("ascii")

    jp = _make_instance()
    payload, signing_input, header_out, signature = jp._load(jwt_token)

    assert payload == payload_bytes
    assert signing_input == (header_b64 + "." + payload_b64).encode("ascii")
    assert header_out == header
    assert signature == signature_bytes

# short: error path - not enough segments raises DecodeError
def test_load_not_enough_segments():
    jwt_token = b"header.payload"  # only one dot; triggers Not enough segments
    jp = _make_instance()
    with pytest.raises(DecodeError) as excinfo:
        jp._load(jwt_token)
    assert "Not enough segments" in str(excinfo.value)

# short: error path - invalid header padding raises DecodeError
def test_load_invalid_header_padding():
    jwt_token = b"header.payload.sig"  # header_segment invalid for base64 decode
    jp = _make_instance()
    with pytest.raises(DecodeError) as excinfo:
        jp._load(jwt_token)
    assert "Invalid header string" in str(excinfo.value)

# short: branch for detached payload form (b64 False) with empty payload segment
def test_load_detached_payload_false_no_payload_segment():
    header = {"b64": False, "alg": "HS256"}
    header_json = json.dumps(header).encode("utf-8")
    header_b64 = _b64url(header_json)

    # empty payload segment to satisfy detached form requirement
    payload_b64 = ""
    signature_bytes = b"signaturebytes-detached"
    signature_b64 = _b64url(signature_bytes)

    jwt_token = (header_b64 + "." + payload_b64 + "." + signature_b64).encode("ascii")

    jp = _make_instance()
    payload, signing_input, header_out, signature = jp._load(jwt_token)

    assert payload == b""
    assert header_out == header
    assert signing_input == (header_b64 + "." + payload_b64).encode("ascii")
    assert signature == signature_bytes
