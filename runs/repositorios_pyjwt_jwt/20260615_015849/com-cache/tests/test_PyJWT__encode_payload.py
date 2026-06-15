import json
import pytest
from datetime import datetime
from repositorios.pyjwt.jwt.api_jwt import PyJWT

# curto: happy path with simple payload
def test_encode_payload_basic_happy_path():
    payload = {"a": 1, "b": True}
    inst = PyJWT.__new__(PyJWT)
    expected = json.dumps(payload, separators=(",", ":"), cls=None).encode("utf-8")
    assert inst._encode_payload(payload) == expected

# curto: utiliza encoder customizado para serializar objects
def test_encode_payload_with_custom_encoder():
    class CustomEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, datetime):
                return o.isoformat()
            return super().default(o)

    payload = {"t": datetime(2020, 1, 2, 3, 4, 5)}
    inst = PyJWT.__new__(PyJWT)
    expected = json.dumps(payload, separators=(",", ":"), cls=CustomEncoder).encode("utf-8")
    assert inst._encode_payload(payload, json_encoder=CustomEncoder) == expected

# curto: headers não afetam a codificação (comportamento ignorado pela implementação)
def test_encode_payload_ignores_headers():
    payload = {"a": 1, "b": 2}
    inst = PyJWT.__new__(PyJWT)
    expected = json.dumps(payload, separators=(",", ":"), cls=None).encode("utf-8")
    assert inst._encode_payload(payload, headers={"kid": "abc"}) == expected

# curto: sem encoder, payload com objeto não serializável deve falhar
def test_encode_payload_raises_on_non_serializable_without_encoder():
    payload = {"t": datetime(2020, 1, 1)}
    inst = PyJWT.__new__(PyJWT)
    with pytest.raises(TypeError):
        inst._encode_payload(payload)
