import pytest
from repositorios.pyjwt.jwt.api_jwt import PyJWT

# happy path: decode returns payload and forwards parameters to decode_complete
def test_decode_happy_path(monkeypatch):
    obj = PyJWT.__new__(PyJWT)

    captured = {}

    def fake_decode_complete(self, jwt, key, algorithms, options, verify=None, detached_payload=None, audience=None, subject=None, issuer=None, leeway=None):
        captured['args'] = {
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
        }
        return {"payload": {"sub": "user1"}}

    monkeypatch.setattr(PyJWT, "decode_complete", fake_decode_complete, raising=True)

    res = obj.decode("token123", "secret", algorithms=["HS256"], options=None, verify=None, detached_payload=None, audience=None, subject=None, issuer=None, leeway=0)

    assert res == {"sub": "user1"}
    assert captured['args']['jwt'] == "token123"
    assert captured['args']['key'] == "secret"
    assert captured['args']['algorithms'] == ["HS256"]

# branch: passing extra kwargs should emit a deprecation warning
def test_decode_warns_on_extra_kwargs(monkeypatch):
    obj = PyJWT.__new__(PyJWT)

    def fake_decode_complete(self, jwt, key, algorithms, options, verify=None, detached_payload=None, audience=None, subject=None, issuer=None, leeway=None):
        return {"payload": {}}

    monkeypatch.setattr(PyJWT, "decode_complete", fake_decode_complete, raising=True)

    with pytest.warns(Warning):
        obj.decode("token", "key", algorithms=["HS256"], extra="x")
