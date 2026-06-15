import warnings
from repositorios.pyjwt.jwt.api_jwt import PyJWT


def _make_pyjwt_instance():
    return object.__new__(PyJWT)

# happy path: decode delegates to decode_complete and returns payload
def test_decode_happy_path_returns_payload():
    obj = _make_pyjwt_instance()

    def fake_decode_complete(self, jwt, key, algorithms, options, verify=None,
                             detached_payload=None, audience=None, subject=None,
                             issuer=None, leeway=0, **kwargs):
        return {'payload': {'user': 'alice'}}

    obj.decode_complete = fake_decode_complete.__get__(obj, PyJWT)

    result = PyJWT.decode(obj, "token", key="secret")
    assert result == {'user': 'alice'}

# warns on extra kwargs and passes through to decode_complete
def test_decode_warns_on_extra_kwargs_emits_warning_and_delegates():
    obj = _make_pyjwt_instance()
    captured_kwargs = {}

    def fake_decode_complete(self, jwt, key, algorithms, options, verify=None,
                             detached_payload=None, audience=None, subject=None,
                             issuer=None, leeway=0, **kwargs):
        captured_kwargs['jwt'] = jwt
        captured_kwargs['key'] = key
        captured_kwargs['kwargs'] = kwargs
        return {'payload': {'ok': True}}

    obj.decode_complete = fake_decode_complete.__get__(obj, PyJWT)

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        payload = PyJWT.decode(obj, "tok", key="k", extra="value")
        assert payload == {'ok': True}
        assert any("Unsupported kwargs" in str(wi.message) for wi in w)
        assert captured_kwargs.get('jwt') == "tok"
        assert captured_kwargs.get('key') == "k"
        # Currently, extra kwargs are not forwarded to decode_complete
        assert captured_kwargs.get('kwargs', {}) == {}

# forwards all provided arguments to decode_complete (verify parameter passthrough)
def test_decode_forwards_all_params_to_decode_complete():
    obj = _make_pyjwt_instance()
    seen = {}

    def fake_decode_complete(self, jwt, key, algorithms, options, verify=None,
                             detached_payload=None, audience=None, subject=None,
                             issuer=None, leeway=0, **kwargs):
        seen['payload_call'] = {
            'jwt': jwt,
            'key': key,
            'algorithms': algorithms,
            'options': options,
            'verify': verify,
            'detached_payload': detached_payload,
            'audience': audience,
            'subject': subject,
            'issuer': issuer,
            'leeway': leeway,
            'kwargs': kwargs
        }
        return {'payload': {'ok': True}}

    obj.decode_complete = fake_decode_complete.__get__(obj, PyJWT)

    res = PyJWT.decode(
        obj,
        "mytoken",
        key="k",
        algorithms=["RS256"],
        options={'verify_signature': True},
        audience="aud",
        subject="sub",
        issuer="iss",
        leeway=2.5
    )

    assert res == {'ok': True}
    call = seen['payload_call']
    assert call['jwt'] == "mytoken"
    assert call['key'] == "k"
    assert call['algorithms'] == ["RS256"]
    assert call['options'] == {'verify_signature': True}
    assert call['audience'] == "aud"
    assert call['subject'] == "sub"
    assert call['issuer'] == "iss"
    assert call['leeway'] == 2.5
