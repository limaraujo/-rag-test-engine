import pytest
from repositorios.pyjwt.jwt.api_jwt import PyJWT


# helper stubs to isolate decode_complete behavior
class DummyJWS:
    def __init__(self, ret):
        self.ret = ret
    def decode_complete(self, jwt, key=None, algorithms=None, options=None, detached_payload=None):
        return self.ret

class DummyPyJWT(PyJWT):
    def __init__(self):
        pass

def build_instance():
    inst = DummyPyJWT()
    inst._jws = DummyJWS({"header": {"alg": "HS256"}, "payload": {"orig": True}, "signature": "sig"})
    inst._decode_payload = lambda decoded: {"decoded": True}
    inst._validate_claims = lambda payload, merged_options, **kwargs: None
    inst._merge_options = lambda options: {}
    return inst

# short: happy path - payload is replaced by decoded payload, header/signature preserved
def test_decode_complete_happy_path_payload_decoded_and_returned():
    # happy path
    inst = build_instance()
    result = inst.decode_complete("token", key="k", algorithms=["HS256"], options=None)
    assert result["header"] == {"alg": "HS256"}
    assert result["signature"] == "sig"
    assert result["payload"] == {"decoded": True}

# short: extra kwargs trigger a warning about deprecated kwargs usage
def test_decode_complete_warns_on_extra_kwargs():
    inst = build_instance()
    with pytest.warns(Warning):
        inst.decode_complete("token", key="k", algorithms=["HS256"], options=None, extra_param="x")

# short: mismatch between verify and verify_signature triggers deprecation warning
def test_decode_complete_warns_on_verify_mismatch():
    inst = build_instance()
    with pytest.warns(DeprecationWarning):
        inst.decode_complete("token", key="k", algorithms=["HS256"], verify=False)

# short: no warning when options.verify_signature is False and verify is not provided
def test_decode_complete_no_warning_with_options_verify_false():
    inst = build_instance()
    result = inst.decode_complete("token", key="k", algorithms=["HS256"], options={"verify_signature": False})
    assert isinstance(result, dict)
