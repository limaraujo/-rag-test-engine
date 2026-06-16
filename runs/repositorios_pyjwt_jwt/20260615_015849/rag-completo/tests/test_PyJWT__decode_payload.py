import json
import pytest
from repositorios.pyjwt.jwt.exceptions import DecodeError
from repositorios.pyjwt.jwt.api_jwt import PyJWT

import json
import pytest

from repositorios.pyjwt.jwt.exceptions import DecodeError
from repositorios.pyjwt.jwt.api_jwt import PyJWT

# happy path
def test__decode_payload_happy_path():
    # Verifica que payload JSON valido retorna dict correspondente
    decoded = {"payload": json.dumps({"foo": "bar", "num": 42})}
    result = PyJWT._decode_payload(None, decoded)
    assert result == {"foo": "bar", "num": 42}

# invalid JSON
def test__decode_payload_invalid_json():
    # Verifica que string não-JSON levanta DecodeError
    decoded = {"payload": "not json"}
    with pytest.raises(DecodeError):
        PyJWT._decode_payload(None, decoded)

# payload JSON não é objeto
def test__decode_payload_json_not_object():
    # Verifica que JSON que não é objeto (ex.: lista) levanta DecodeError
    decoded = {"payload": json.dumps([1, 2, 3])}
    with pytest.raises(DecodeError):
        PyJWT._decode_payload(None, decoded)
