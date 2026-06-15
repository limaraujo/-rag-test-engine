import pytest
from types import SimpleNamespace
from datetime import datetime
from calendar import timegm
from repositorios.pyjwt.jwt.api_jwt import PyJWT



# helper to create a PyJWT instance with mocked internals
def _make_fake_jwt():
    jwt = PyJWT.__new__(PyJWT)
    captured = {}

    def fake_encode_payload(payload, headers=None, json_encoder=None):
        captured['payload'] = payload
        captured['headers'] = headers
        captured['json_encoder'] = json_encoder
        return "ENCODED"

    def fake_jws_encode(json_payload, key, algorithm, headers, json_encoder, sort_headers=True):
        captured['json_payload'] = json_payload
        captured['key'] = key
        captured['algorithm'] = algorithm
        captured['headers'] = headers
        captured['json_encoder'] = json_encoder
        captured['sort_headers'] = sort_headers
        return "TOKEN"

    jwt._encode_payload = fake_encode_payload
    jwt._jws = SimpleNamespace(encode=fake_jws_encode)
    return jwt, captured


# short: happy path
# verifies that payload dict is accepted, _encode_payload is called with the payload,
# and the final token is produced by _jws.encode with the correct parameters
def test_encode_happy_path_calls_encode_payload_and_jws():
    jwt, captured = _make_fake_jwt()

    payload = {"sub": "alice"}
    token = jwt.encode(payload=payload, key="secret-key", algorithm=None, headers={"kid": "key1"}, json_encoder=None, sort_headers=True)

    assert token == "TOKEN"
    # _encode_payload should receive the payload (copy semantics)
    assert captured['payload'] == payload
    assert captured['headers'] == {"kid": "key1"}
    assert captured['json_encoder'] is None
    # _jws.encode should receive the encoded payload and original call parameters
    assert captured['json_payload'] == "ENCODED"
    assert captured['key'] == "secret-key"
    assert captured['headers'] == {"kid": "key1"}
    assert captured['sort_headers'] is True


# short: non-dict payload should raise TypeError
# verifies that a non-dict payload triggers the documented TypeError
def test_encode_raises_type_error_on_non_dict_payload():
    jwt, _ = _make_fake_jwt()
    with pytest.raises(TypeError) as excinfo:
        jwt.encode(payload=[1, 2, 3], key="secret-key")
    assert "Expecting a dict object" in str(excinfo.value)


# short: iss not string should raise TypeError
# verifies that non-string issuer raises the specific error
def test_encode_issuer_not_string_raises_type_error():
    jwt, _ = _make_fake_jwt()
    payload = {"iss": 123}
    with pytest.raises(TypeError) as excinfo:
        jwt.encode(payload=payload, key="secret-key")
    assert "Issuer (iss) must be a string." in str(excinfo.value)


# short: datetime claims are converted to int timestamps
# ensures exp/iat/nbf datetime values are converted using timegm before encoding
def test_encode_converts_datetime_time_claims_to_int():
    jwt, captured = _make_fake_jwt()

    dt_exp = datetime(2020, 1, 1, 0, 0, 0)
    dt_iat = datetime(2020, 1, 1, 1, 0, 0)
    dt_nbf = datetime(2020, 1, 1, 2, 0, 0)

    payload = {"exp": dt_exp, "iat": dt_iat, "nbf": dt_nbf}
    jwt.encode(payload=payload, key="secret-key")

    # verify conversion for each time-based claim
    converted_exp = timegm(dt_exp.utctimetuple())
    converted_iat = timegm(dt_iat.utctimetuple())
    converted_nbf = timegm(dt_nbf.utctimetuple())

    assert captured['payload']['exp'] == converted_exp
    assert captured['payload']['iat'] == converted_iat
    assert captured['payload']['nbf'] == converted_nbf
