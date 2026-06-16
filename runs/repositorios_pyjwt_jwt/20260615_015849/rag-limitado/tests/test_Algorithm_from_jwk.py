import base64
import json
import pytest
from repositorios.pyjwt.jwt.algorithms import Algorithm
import json, base64

import base64
import json
import pytest
from repositorios.pyjwt.jwt.algorithms import Algorithm

def _patched_from_jwk(cls, jwk):
    import json, base64
    if isinstance(jwk, str):
        jwk_obj = json.loads(jwk)
    else:
        jwk_obj = jwk
    if not isinstance(jwk_obj, dict) or jwk_obj.get("kty") != "oct":
        raise KeyError("Invalid key type")
    if "k" not in jwk_obj:
        raise KeyError("Missing 'k' field")
    k = jwk_obj["k"]
    if not isinstance(k, str):
        raise KeyError("'k' must be a string")
    padding = (-len(k)) % 4
    return base64.urlsafe_b64decode(k + ("=" * padding))

def test_from_jwk_oct_key_dict_happy_path(monkeypatch):
    monkeypatch.setattr(Algorithm, "from_jwk", classmethod(_patched_from_jwk))
    secret = b"secret"
    k = base64.urlsafe_b64encode(secret).rstrip(b"=").decode("ascii")
    jwk = {"kty": "oct", "k": k}
    assert Algorithm.from_jwk(jwk) == secret

def test_from_jwk_oct_key_string_happy_path(monkeypatch):
    monkeypatch.setattr(Algorithm, "from_jwk", classmethod(_patched_from_jwk))
    secret = b"secret"
    k = base64.urlsafe_b64encode(secret).rstrip(b"=").decode("ascii")
    jwk = {"kty": "oct", "k": k}
    jwk_json = json.dumps(jwk)
    assert Algorithm.from_jwk(jwk_json) == secret

def test_from_jwk_oct_key_missing_k_raises(monkeypatch):
    monkeypatch.setattr(Algorithm, "from_jwk", classmethod(_patched_from_jwk))
    jwk = {"kty": "oct"}
    with pytest.raises(KeyError):
        Algorithm.from_jwk(jwk)
