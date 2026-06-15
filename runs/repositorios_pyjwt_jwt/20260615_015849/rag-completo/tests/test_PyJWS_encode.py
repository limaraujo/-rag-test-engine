import json
import pytest
from types import MethodType
from repositorios.pyjwt.jwt.exceptions import InvalidKeyError
from repositorios.pyjwt.jwt.utils import base64url_decode
from repositorios.pyjwt.jwt.api_jws import PyJWS

# helper to build a minimal PyJWS-like instance with controllable algorithm behavior
def _make_pyjws_instance(key_len_msg=None, enforce_minimum=False):
    obj = object.__new__(PyJWS)
    obj.header_typ = "JWT"
    obj.options = {"enforce_minimum_key_length": enforce_minimum}

    def _validate_headers(self, headers, encoding=True):
        return None

    obj._validate_headers = MethodType(_validate_headers, obj)

    def _get_algorithm_by_name(self, name):
        class _FakeAlg:
            def prepare_key(self, key):
                return key

            def check_key_length(self, key):
                return key_len_msg

            def sign(self, msg, key):
                return b"sig"
        return _FakeAlg()

    obj.get_algorithm_by_name = MethodType(_get_algorithm_by_name, obj)
    return obj


# 1) Happy path: basic encode with default algorithm (HS256), no headers, payload encoded
def test_encode_basic_happy_path():
    # brief: happy path - default algorithm and simple payload/key
    pyjws = _make_pyjws_instance(key_len_msg=None, enforce_minimum=False)
    payload = b"payload"
    key = b"secret"

    encoded = pyjws.encode(payload, key)

    header_b64, payload_b64, sig_b64 = encoded.split(".")
    header_json = base64url_decode(header_b64.encode()).decode("utf-8")
    header = json.loads(header_json)

    assert header.get("typ") == "JWT"
    assert header.get("alg") == "HS256"
    assert base64url_decode(payload_b64.encode()) == payload
    assert base64url_decode(sig_b64.encode()) == b"sig"


# 2) Headers override alg and request detached payload (b64 False) -> payload should be empty
def test_encode_headers_alg_override_and_detached_payload():
    pyjws = _make_pyjws_instance(key_len_msg=None, enforce_minimum=False)
    payload = b"payload"
    key = b"secret"
    headers = {"alg": "RS256", "b64": False}

    encoded = pyjws.encode(payload, key, headers=headers)

    header_b64, payload_b64, sig_b64 = encoded.split(".")
    header_json = base64url_decode(header_b64.encode()).decode("utf-8")
    header = json.loads(header_json)

    # alg must come from headers override
    assert header.get("alg") == "RS256"
    # since b64 is False, payload should be detached (empty)
    assert payload_b64 == "" or base64url_decode(payload_b64.encode()) == b""
    # b64 header should be present and indicate detachment
    assert header.get("b64") is False
    # ensure "crit" contains "b64" due to RFC 7797
    crit = header.get("crit")
    assert isinstance(crit, list) and "b64" in crit

    # signature still decodes to the deterministic fake value
    assert base64url_decode(sig_b64.encode()) == b"sig"


# 3) Explicit algorithm=None path: alg should be "none" for non-PyJWK key
def test_encode_algorithm_none_when_none_provided():
    pyjws = _make_pyjws_instance(key_len_msg=None, enforce_minimum=False)
    payload = b"payload"
    key = b"secret"

    encoded = pyjws.encode(payload, key, algorithm=None)

    header_b64, payload_b64, sig_b64 = encoded.split(".")
    header_json = base64url_decode(header_b64.encode()).decode("utf-8")
    header = json.loads(header_json)

    assert header.get("alg") == "none"
    assert base64url_decode(payload_b64.encode()) == payload
    assert base64url_decode(sig_b64.encode()) == b"sig"


# 4) Key length enforcement raises InvalidKeyError when key too short and enforcement is enabled
def test_encode_key_length_enforcement_raises():
    pyjws = _make_pyjws_instance(key_len_msg="too short", enforce_minimum=True)
    payload = b"payload"
    key = b"short"

    with pytest.raises(InvalidKeyError):
        pyjws.encode(payload, key)
