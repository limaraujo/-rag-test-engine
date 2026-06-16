import json
from decimal import Decimal
from repositorios.pyjwt.jwt.api_jwt import PyJWT

# curto: happy path basic encoding without custom encoder
def test_encode_payload_basic_happy_path():
    obj = PyJWT.__new__(PyJWT)
    payload = {"a": 1, "b": "x"}
    result = PyJWT._encode_payload(obj, payload)
    expected = json.dumps(payload, separators=(",", ":"), cls=None).encode("utf-8")
    assert result == expected

# curto: usar encoder personalizado para tipos não nativos
def test_encode_payload_with_custom_encoder_decimals():
    class DecimalEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, Decimal):
                return float(o)
            return super().default(o)

    obj = PyJWT.__new__(PyJWT)
    payload = {"value": Decimal("1.5")}
    result = PyJWT._encode_payload(obj, payload, json_encoder=DecimalEncoder)
    expected = json.dumps(payload, separators=(",", ":"), cls=DecimalEncoder).encode("utf-8")
    assert result == expected

# curto: headers não afetam a saída (teste de ignorância de parâmetro não utilizado)
def test_encode_payload_ignores_headers_param():
    obj = PyJWT.__new__(PyJWT)
    payload = {"k": "v"}
    headers = {"typ": "JWT"}
    res_with_headers = PyJWT._encode_payload(obj, payload, headers)
    res_without_headers = PyJWT._encode_payload(obj, payload)
    assert res_with_headers == res_without_headers

# curto: verifica que os separadores usados não incluem espaços
def test_encode_payload_uses_no_spaces_between_items():
    obj = PyJWT.__new__(PyJWT)
    payload = {"a": 1, "b": 2}
    s = PyJWT._encode_payload(obj, payload).decode("utf-8")
    assert ", " not in s
    assert ": " not in s
