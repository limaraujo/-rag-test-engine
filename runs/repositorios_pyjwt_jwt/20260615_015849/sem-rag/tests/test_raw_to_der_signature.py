import pytest
import repositorios.pyjwt.jwt.utils as utils
from repositorios.pyjwt.jwt.utils import raw_to_der_signature

# happy path: curva de 256 bits, r=1 e s=2 via bytes_to_number; encode_dss_signature retorna b"DER"
def test_happy_path_calls_encode_with_correct_r_s(monkeypatch):
    returns = iter([1, 2])
    captured = {}
    def fake_bytes_to_number(_):
        return next(returns)
    def fake_encode_dss_signature(r, s):
        captured['r'] = r
        captured['s'] = s
        return b"DER"
    monkeypatch.setattr(utils, "bytes_to_number", fake_bytes_to_number)
    monkeypatch.setattr(utils, "encode_dss_signature", fake_encode_dss_signature)
    class FakeCurve:
        key_size = 256
    num_bytes = 32
    raw_sig = (1).to_bytes(num_bytes, "big") + (2).to_bytes(num_bytes, "big")
    result = utils.raw_to_der_signature(raw_sig, FakeCurve())
    assert result == b"DER"
    assert captured == {'r': 1, 's': 2}

# edge case: input length inválido levanta ValueError
def test_invalid_input_length_raises_value_error():
    class FakeCurve:
        key_size = 256
    raw_sig = b"\x00" * 63  # 1 byte short for 256-bit curve (needs 64 bytes)
    with pytest.raises(ValueError):
        utils.raw_to_der_signature(raw_sig, FakeCurve())

# path with different key_size (128 bits): verifica uso correto de num_bytes e passagem de r,s
def test_happy_path_with_different_key_size_checks_num_bytes(monkeypatch):
    captured = []
    returns = iter([123, 456])
    def fake_bytes_to_number(_):
        return next(returns)
    def fake_encode_dss_signature(r, s):
        captured.append((r, s))
        return b"OK"
    monkeypatch.setattr(utils, "bytes_to_number", fake_bytes_to_number)
    monkeypatch.setattr(utils, "encode_dss_signature", fake_encode_dss_signature)
    class FakeCurve:
        key_size = 128
    num_bytes = (128 + 7) // 8  # 16
    raw_sig = (123).to_bytes(num_bytes, "big") + (456).to_bytes(num_bytes, "big")
    result = utils.raw_to_der_signature(raw_sig, FakeCurve())
    assert result == b"OK"
    assert captured == [(123, 456)]
