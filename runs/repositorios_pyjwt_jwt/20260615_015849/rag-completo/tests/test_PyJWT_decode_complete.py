import warnings
from repositorios.pyjwt.jwt.api_jwt import PyJWT

# test 1: happy path - default options flow, payload decoding and validation chain invoked
def test_decode_complete_happy_path_integration():
    PyJWTCls = PyJWT
    pj = object.__new__(PyJWTCls)

    class DummyJWS:
        def __init__(self, ret=None):
            self.ret = ret or {'header': {'alg': 'HS256'}, 'payload': {'data': 1}, 'signature': 'sig'}
            self.last_options = None
        def decode_complete(self, jwt, key=None, algorithms=None, options=None, detached_payload=None, **kwargs):
            self.last_options = options
            return self.ret

    dummy = DummyJWS()
    pj._jws = dummy
    pj._merge_options = lambda options: {}
    def decode_payload(decoded):
        return {'payload_decoded': decoded['payload']}
    pj._decode_payload = decode_payload

    captured = {}
    def validate_claims(payload, merged_options, audience=None, issuer=None, leeway=None, subject=None):
        captured['payload'] = payload
        captured['merged_options'] = merged_options
        captured['audience'] = audience
        captured['issuer'] = issuer
        captured['leeway'] = leeway
        captured['subject'] = subject
    pj._validate_claims = validate_claims

    res = pj.decode_complete(jwt='jwt', key='k', algorithms=['HS256'], options=None, leeway=None)

    assert res == {'header': {'alg': 'HS256'}, 'payload': {'payload_decoded': {'data': 1}}, 'signature': 'sig'}
    assert captured['payload'] == {'payload_decoded': {'data': 1}}
    assert captured['audience'] is None
    assert captured['issuer'] is None
    assert captured['leeway'] is None
    assert captured['subject'] is None
    assert dummy.last_options == {'verify_signature': True, 'enforce_minimum_key_length': False}

# test 2: kwargs deprecation path - extra kwargs should trigger a warning but not disrupt execution
def test_decode_complete_warns_on_extra_kwargs():
    PyJWTCls = PyJWT
    pj = object.__new__(PyJWTCls)

    class DummyJWS:
        def __init__(self, ret=None):
            self.ret = ret or {'header': {'alg': 'HS256'}, 'payload': {'x': 2}, 'signature': 'sig'}
            self.last_options = None
        def decode_complete(self, jwt, key=None, algorithms=None, options=None, detached_payload=None, **kwargs):
            self.last_options = options
            return self.ret

    dummy = DummyJWS()
    pj._jws = dummy
    pj._merge_options = lambda options: {}
    def decode_payload(decoded):
        return {'payload_decoded': decoded['payload']}
    pj._decode_payload = decode_payload
    pj._validate_claims = lambda payload, merged_options, audience=None, issuer=None, leeway=None, subject=None: None

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        res = pj.decode_complete(jwt='jwt', key='k', algorithms=['HS256'], options=None, extra='x')
        # ensure execution continued and a warning about extra kwargs was emitted
        assert res['header'] == {'alg': 'HS256'}
        assert any('kwargs' in str(wr.message) for wr in w)

# test 3: verify argument mismatch path - mismatching verify arg vs options should warn
def test_decode_complete_warns_on_verify_mismatch():
    PyJWTCls = PyJWT
    pj = object.__new__(PyJWTCls)

    class DummyJWS:
        def __init__(self, ret=None):
            self.ret = ret or {'header': {'alg': 'HS256'}, 'payload': {'y': 3}, 'signature': 'sig'}
        def decode_complete(self, jwt, key=None, algorithms=None, options=None, detached_payload=None, **kwargs):
            return self.ret

    dummy = DummyJWS()
    pj._jws = dummy
    pj._merge_options = lambda options: {}
    pj._decode_payload = lambda decoded: {'payload_decoded': decoded['payload']}
    pj._validate_claims = lambda payload, merged_options, audience=None, issuer=None, leeway=None, subject=None: None

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        res = pj.decode_complete(jwt='jwt', key='k', algorithms=['HS256'], verify=False)
        assert res['header'] == {'alg': 'HS256'}
        assert any('The `verify` argument' in str(wr.message) for wr in w)

# test 4: options.verify_signature False path - ensure the jws decode is invoked with proper sig_options
def test_decode_complete_options_verify_signature_false_passed():
    PyJWTCls = PyJWT
    pj = object.__new__(PyJWTCls)

    class DummyJWS:
        def __init__(self, ret=None):
            self.ret = ret or {'header': {'alg': 'HS256'}, 'payload': {'z': 9}, 'signature': 'sig'}
        def decode_complete(self, jwt, key=None, algorithms=None, options=None, detached_payload=None, **kwargs):
            # ensure we pass through verify_signature False
            assert options == {'verify_signature': False, 'enforce_minimum_key_length': False}
            return self.ret

    dummy = DummyJWS()
    pj._jws = dummy
    pj._merge_options = lambda options: {}
    pj._decode_payload = lambda decoded: {'payload_decoded': decoded['payload']}
    pj._validate_claims = lambda payload, merged_options, audience=None, issuer=None, leeway=None, subject=None: None

    res = pj.decode_complete(jwt='jwt', key='k', algorithms=['HS256'], options={'verify_signature': False})

    assert res == {'header': {'alg': 'HS256'}, 'payload': {'payload_decoded': {'z': 9}}, 'signature': 'sig'}
