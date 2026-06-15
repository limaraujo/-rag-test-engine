import json
import pytest
from repositorios.pyjwt.jwt.exceptions import PyJWKSetError
from repositorios.pyjwt.jwt.api_jwk import PyJWKSet

import json
import pytest

from repositorios.pyjwt.jwt.exceptions import PyJWKSetError
from repositorios.pyjwt.jwt.api_jwk import PyJWKSet


# short: happy path - ensure from_json delegates to from_dict after json.loads
def test_from_json_happy_path(monkeypatch):
    sentinel = object()

    def fake_from_dict(cls, obj):
        return sentinel

    monkeypatch.setattr(PyJWKSet, "from_dict", classmethod(fake_from_dict))
    monkeypatch.setattr(json, "loads", lambda s: {"keys": []})

    assert PyJWKSet.from_json('{"keys": []}') is sentinel


# short: invalid JSON should raise JSONDecodeError
def test_from_json_invalid_json_raises_json_decode_error():
    with pytest.raises(json.JSONDecodeError):
        PyJWKSet.from_json('{"keys": [}')


# short: propagate PyJWKSetError raised by from_dict
def test_from_json_from_dict_raises_pyjwkseterror(monkeypatch):
    def _raise(cls, obj):
        raise PyJWKSetError("boom")

    monkeypatch.setattr(PyJWKSet, "from_dict", classmethod(_raise))
    monkeypatch.setattr(json, "loads", lambda s: {"keys": []})

    with pytest.raises(PyJWKSetError):
        PyJWKSet.from_json('{"keys": []}')


# short: ensure dict parsed by json.loads is forwarded to from_dict
def test_from_json_passes_parsed_dict_to_from_dict(monkeypatch):
    parsed = {"a": 1}

    monkeypatch.setattr(json, "loads", lambda s: parsed)

    recorded = {}

    def _record(cls, obj):
        recorded["obj"] = obj
        return "ok"

    monkeypatch.setattr(PyJWKSet, "from_dict", classmethod(_record))

    assert PyJWKSet.from_json('{"a":1}') == "ok"
    assert recorded["obj"] is parsed
