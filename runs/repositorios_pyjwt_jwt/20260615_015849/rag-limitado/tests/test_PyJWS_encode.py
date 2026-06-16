import base64
import json
import pytest
import types
from repositorios.pyjwt.jwt.exceptions import InvalidTokenError
from repositorios.pyjwt.jwt.api_jws import PyJWS

import base64
import json
import pytest
import types

from repositorios.pyjwt.jwt.exceptions import InvalidTokenError
from repositorios.pyjwt.jwt.api_jws import PyJWS

# Helper to create a minimal PyJWS instance without invoking __init__
def _make_fake_pyjws():
    pyjws = object.__new__(PyJWS)
    pyjws.header_typ = "JWT"
    pyjws.options = {"enforce_minimum_key_length": False}

    def _validate_headers(self, headers, encoding=True):
        return None

    pyjws._validate_headers = types.MethodType(_validate_headers, pyjws)

    def _get_algorithm_by_name(name=None):
        class DummyAlg:
            def check_key_length(self, key):
                return None
            def prepare_key(self, key):
                return key
            def sign(self, signing_input, key):
                return b"sig"
        return DummyAlg()

    pyjws.get_algorithm_by_name = _get_algorithm_by_name
    return pyjws

# Helpers for base64url decoding (no padding)
def _b64url_decode(seg: str) -> bytes:
    if seg == "":
        return b""
    padding = "=" * (-len(seg) % 4)
    return base64.urlsafe_b64decode(seg + padding)

def _b64url_decode_to_str(seg: str) -> str:
    if seg == "":
        return ""
    return _b64url_decode(seg).decode("utf-8")

# 1) Happy path: simple payload, no headers, standard signing
def test_encode_happy_path():
    # corto: verify normal flow produces header/payload/signature segments correspondingly
    pyjws = _make_fake_pyjws()
    payload = b"payload"
    key = b"secret"
    result = pyjws.encode(
        payload=payload,
        key=key,
        algorithm="HS256",
        headers=None,
        json_encoder=None,
        is_payload_detached=False,
        sort_headers=True,
    )

    segments = result.split(".")
    assert len(segments) == 3

    header_json = _b64url_decode_to_str(segments[0])
    header = json.loads(header_json)
    assert header.get("typ") == "JWT"
    assert header.get("alg") == "HS256"

    # payload decodes to original payload
    payload_dec = _b64url_decode(segments[1])
    assert payload_dec == payload

    # signature decodes to "sig"
    sig_dec = _b64url_decode(segments[2])
    assert sig_dec == b"sig"

# 2) Branch: detached payload is allowed; payload segment should be empty
def test_encode_detached_payload_header_includes_b64_and_crit():
    pyjws = _make_fake_pyjws()
    payload = b"payload-detached"
    result = pyjws.encode(
        payload=payload,
        key=b"secret",
        algorithm="HS256",
        headers=None,
        json_encoder=None,
        is_payload_detached=True,
        sort_headers=True,
    )

    segments = result.split(".")
    assert len(segments) == 3

    # header should include b64=False and a crit containing "b64"
    header = json.loads(_b64url_decode_to_str(segments[0]))
    assert header.get("alg") == "HS256"
    assert header.get("typ") == "JWT"
    assert header.get("b64") is False
    assert header.get("crit") == ["b64"]

    # payload segment should be empty
    assert segments[1] == ""

    # signature decodes to "sig"
    assert _b64url_decode(segments[2]) == b"sig"

# 3) Exception path: invalid 'crit' header value (not a list) when detached
def test_encode_raises_InvalidTokenError_for_bad_crit_header():
    pyjws = _make_fake_pyjws()
    with pytest.raises(InvalidTokenError):
        pyjws.encode(
            payload=b"payload",
            key=b"secret",
            algorithm="HS256",
            headers={"crit": "notalist"},
            json_encoder=None,
            is_payload_detached=True,
            sort_headers=True,
        )

# 4) If headers include a 'b64' key and not detached, it should be removed from the final header
def test_encode_removes_b64_when_header_provided():
    pyjws = _make_fake_pyjws()
    payload = b"payload4"
    result = pyjws.encode(
        payload=payload,
        key=b"secret",
        algorithm="HS256",
        headers={"b64": True},
        json_encoder=None,
        is_payload_detached=False,
        sort_headers=True,
    )

    segments = result.split(".")
    assert len(segments) == 3

    header = json.loads(_b64url_decode_to_str(segments[0]))
    # b64 should be removed in final header
    assert "b64" not in header
    assert header.get("alg") == "HS256"
    assert header.get("typ") == "JWT"

    # payload decodes to original payload
    assert _b64url_decode(segments[1]) == payload

    # signature decodes to "sig"
    assert _b64url_decode(segments[2]) == b"sig"
