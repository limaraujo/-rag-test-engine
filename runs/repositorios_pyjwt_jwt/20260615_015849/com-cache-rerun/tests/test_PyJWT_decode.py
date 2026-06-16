import pytest
from repositorios.pyjwt.jwt.api_jwt import PyJWT

# verifica o caminho feliz: decode delega para decode_complete e retorna payload
def test_decode_happy_path_returns_payload(monkeypatch):
    captured = {}

    def fake_decode_complete(self, jwt, key, algorithms, options, verify=None,
                           detached_payload=None, audience=None, subject=None,
                           issuer=None, leeway=None, **kwargs):
        captured.update({
            "jwt": jwt,
            "key": key,
            "algorithms": algorithms,
            "options": options,
            "verify": verify,
            "detached_payload": detached_payload,
            "audience": audience,
            "subject": subject,
            "issuer": issuer,
            "leeway": leeway,
            "kwargs": kwargs,
        })
        return {"payload": {"user": "alice"}}

    monkeypatch.setattr(PyJWT, "decode_complete", fake_decode_complete, raising=True)
    jwt_instance = PyJWT()
    result = jwt_instance.decode("token123", key="secret", algorithms=["HS256"])
    assert result == {"user": "alice"}
    assert captured["jwt"] == "token123"

# verifica aviso gerado ao passar kwargs adicionais (caminho de erro/obsoleto)
def test_decode_warns_on_extra_kwargs(monkeypatch):
    def fake_decode_complete(self, jwt, key, algorithms, options, verify=None,
                           detached_payload=None, audience=None, subject=None,
                           issuer=None, leeway=None, **kwargs):
        return {"payload": {"ok": True}}

    monkeypatch.setattr(PyJWT, "decode_complete", fake_decode_complete, raising=True)
    jwt_instance = PyJWT()
    with pytest.warns(Warning):
        result = jwt_instance.decode("tok", key="k", extra="value")
    assert result == {"ok": True}

# verifica passagem de argumentos através para decode_complete
def test_decode_passes_through_arguments(monkeypatch):
    captured = {}

    def fake_decode_complete(self, jwt, key, algorithms, options, verify=None,
                           detached_payload=None, audience=None, subject=None,
                           issuer=None, leeway=None, **kwargs):
        captured.update({
            "jwt": jwt,
            "key": key,
            "algorithms": algorithms,
            "options": options,
            "verify": verify,
            "detached_payload": detached_payload,
            "audience": audience,
            "subject": subject,
            "issuer": issuer,
            "leeway": leeway,
        })
        return {"payload": {}}

    monkeypatch.setattr(PyJWT, "decode_complete", fake_decode_complete, raising=True)
    jwt_instance = PyJWT()
    jwt_instance.decode(
        "tokX",
        key="k",
        algorithms=["RS256"],
        options={"foo": "bar"},
        verify=True,
        detached_payload=b"payload",
        audience="aud1",
        subject="subj",
        issuer=["iss1"],
        leeway=5.0,
    )

    assert captured["jwt"] == "tokX"
    assert captured["key"] == "k"
    assert captured["algorithms"] == ["RS256"]
    assert captured["options"] == {"foo": "bar"}
    assert captured["verify"] is True
    assert captured["detached_payload"] == b"payload"
    assert captured["audience"] == "aud1"
    assert captured["subject"] == "subj"
    assert captured["issuer"] == ["iss1"]
    assert captured["leeway"] == 5.0
