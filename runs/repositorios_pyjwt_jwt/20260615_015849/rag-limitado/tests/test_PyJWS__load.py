import base64
import json
import pytest
from repositorios.pyjwt.jwt.exceptions import DecodeError
from repositorios.pyjwt.jwt.api_jws import PyJWS

import base64
import json
import pytest

from repositorios.pyjwt.jwt.exceptions import DecodeError
from repositorios.pyjwt.jwt.api_jws import PyJWS

def _b64u(b: bytes) -> bytes:
    return base64.urlsafe_b64encode(b).rstrip(b"=")

# short: happy path and b64=false branch
@pytest.mark.parametrize("scenario", ["normal", "b64_false"])
def test_load_basic_scenarios(scenario):
    # short: verify normal decoding and detached payload mode when b64 is false
    pyjws = PyJWS()

    header = {"alg": "HS256"}
    payload = b"payload-data"
    signature = b"signature-bytes"

    header_b64 = _b64u(json.dumps(header).encode("utf-8"))
    payload_b64 = _b64u(payload)
    sig_b64 = _b64u(signature)

    if scenario == "normal":
        signing_input = header_b64 + b"." + payload_b64
        token = signing_input + b"." + sig_b64
        payload_out, signing_input_out, header_out, signature_out = pyjws._load(token)
        assert payload_out == payload
        assert signing_input_out == signing_input
        assert header_out == header
        assert signature_out == signature
    else:  # scenario == "b64_false"
        # b64: False means payload must be empty; the token has an empty payload segment
        header_with_b64_false = {"alg": "HS256", "b64": False}
        header_b64_false = _b64u(json.dumps(header_with_b64_false).encode("utf-8"))
        signing_input = header_b64_false + b"." + b""  # empty payload segment
        token = signing_input + b"." + sig_b64
        payload_out, signing_input_out, header_out, signature_out = pyjws._load(token)
        assert payload_out == b""
        assert signing_input_out == signing_input
        assert header_out == header_with_b64_false
        assert signature_out == signature

# short: invalid header padding and invalid header JSON
@pytest.mark.parametrize("case", ["invalid_header_padding", "invalid_header_json"])
def test_load_header_parsing_errors(case):
    pyjws = PyJWS()
    payload = b"payload"
    payload_b64 = _b64u(payload)
    signature = b"sig"
    sig_b64 = _b64u(signature)

    if case == "invalid_header_padding":
        header_segment = b"!!"  # invalid base64
        signing_input = header_segment + b"." + payload_b64
        token = signing_input + b"." + sig_b64
        with pytest.raises(DecodeError):
            pyjws._load(token)
    else:  # "invalid_header_json"
        header_segment = base64.urlsafe_b64encode(b"not json").rstrip(b"=")
        signing_input = header_segment + b"." + payload_b64
        token = signing_input + b"." + sig_b64
        with pytest.raises(DecodeError):
            pyjws._load(token)

# short: not enough segments (edge/invalid structure)
def test_load_not_enough_segments():
    pyjws = PyJWS()
    token = b"header.payload"  # only one dot, missing signature
    with pytest.raises(DecodeError):
        pyjws._load(token)
