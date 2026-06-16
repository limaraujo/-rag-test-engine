import pytest
from repositorios.pyjwt.jwt.api_jwt import PyJWT



def _make_stubbed_pyjwt():
    pyjwt = PyJWT()

    class DummyJWS:
        def __init__(self):
            self.called_with = None

        def decode_complete(self, jwt, key=None, algorithms=None, options=None, detached_payload=None):
            self.called_with = {
                "jwt": jwt,
                "key": key,
                "algorithms": algorithms,
                "options": options,
                "detached_payload": detached_payload,
            }
            return {"header": {"alg": "none"}, "signature": "sig"}

    dummy = DummyJWS()
    pyjwt._jws = dummy
    pyjwt._decode_payload = lambda decoded: {"sub": "123"}
    pyjwt._validate_claims = lambda payload, merged_options, audience=None, issuer=None, leeway=None, subject=None: None
    pyjwt._merge_options = lambda options: {} if options is None else options
    return pyjwt, dummy


# Test 1: happy path - default behavior returns header, payload, signature with decoded payload integrated
def test_decode_complete_basic_happy_path():
    # happy path: basic decoding flow with default options and no extra kwargs
    pyjwt, dummy = _make_stubbed_pyjwt()
    result = pyjwt.decode_complete(
        "token",
        key="k",
        algorithms=["HS256"],
        options=None,
        verify=None,
        detached_payload=None,
        audience=None,
        issuer=None,
        subject=None,
        leeway=0,
    )

    assert result == {"header": {"alg": "none"}, "signature": "sig", "payload": {"sub": "123"}}
    assert dummy.called_with["key"] == "k"
    assert dummy.called_with["algorithms"] == ["HS256"]
    assert dummy.called_with["options"] == {"verify_signature": True, "enforce_minimum_key_length": False}
    assert result["payload"] == {"sub": "123"}


# Test 2: ensure options with verify_signature False propagates to jws.decode_complete
def test_decode_complete_with_options_verify_signature_false():
    pyjwt, dummy = _make_stubbed_pyjwt()
    result = pyjwt.decode_complete(
        "token",
        key="k",
        algorithms=["HS256"],
        options={"verify_signature": False},
        verify=None,
        detached_payload=None,
        audience=None,
        issuer=None,
        subject=None,
        leeway=0,
    )

    assert dummy.called_with["options"] == {"verify_signature": False, "enforce_minimum_key_length": False}
    assert result == {"header": {"alg": "none"}, "signature": "sig", "payload": {"sub": "123"}}


# Test 3: ensure a warning is issued when extra kwargs are passed to decode_complete (deprecated behavior)
def test_decode_complete_warns_on_extra_kwargs():
    pyjwt, _ = _make_stubbed_pyjwt()
    with pytest.warns(Warning) as w:
        result = pyjwt.decode_complete("token", foo="bar")

    assert any("passing additional kwargs" in str(record.message) for record in w)
    assert result == {"header": {"alg": "none"}, "signature": "sig", "payload": {"sub": "123"}}


# Test 4: ensure a deprecation warning is emitted when verify arg mismatches the internal option
def test_decode_complete_warns_on_verify_mismatch():
    pyjwt, _ = _make_stubbed_pyjwt()
    with pytest.warns(DeprecationWarning):
        pyjwt.decode_complete("token", verify=False)
