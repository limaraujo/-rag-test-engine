import pytest
from repositorios.pyjwt.jwt.api_jwk import PyJWK

# curto
@pytest.mark.parametrize("algorithm", ["RS256", None])
def test_from_dict_forwards_arguments_to_constructor(monkeypatch, algorithm):
    obj = {"kty": "oct", "alg": "HS256", "kid": "1"}
    captured = {}

    def fake_init(self, obj_param, algorithm_param=None):
        captured["obj"] = obj_param
        captured["alg"] = algorithm_param

    monkeypatch.setattr(PyJWK, "__init__", fake_init, raising=True)

    instance = PyJWK.from_dict(obj, algorithm)

    assert isinstance(instance, PyJWK)
    assert captured["obj"] is obj
    assert captured["alg"] == algorithm
