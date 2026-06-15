from types import SimpleNamespace
import repositorios.pyjwt.jwt.utils as utils_module
from repositorios.pyjwt.jwt.utils import der_to_raw_signature

# happy path: 256-bit curve, r=1, s=2
def test_der_to_raw_signature_happy_path(monkeypatch):
    curve = SimpleNamespace(key_size=256)

    captured = {}

    def fake_decode_dss_signature(der_sig):
        captured['der_sig'] = der_sig
        return (1, 2)

    def fake_number_to_bytes(val, length):
        return int(val).to_bytes(length, 'big')

    monkeypatch.setattr(utils_module, 'decode_dss_signature', fake_decode_dss_signature)
    monkeypatch.setattr(utils_module, 'number_to_bytes', fake_number_to_bytes)

    res = der_to_raw_signature(b"der", curve)
    expected = (1).to_bytes(32, 'big') + (2).to_bytes(32, 'big')
    assert res == expected
    assert captured['der_sig'] == b"der"

# scenario with 128-bit key_size: ensure correct byte length per curve
def test_der_to_raw_signature_uses_128bit_length(monkeypatch):
    curve = SimpleNamespace(key_size=128)

    def fake_decode(der_sig):
        return (3, 4)

    def fake_number_to_bytes(val, length):
        return int(val).to_bytes(length, 'big')

    monkeypatch.setattr(utils_module, 'decode_dss_signature', fake_decode)
    monkeypatch.setattr(utils_module, 'number_to_bytes', fake_number_to_bytes)

    res = der_to_raw_signature(b"der128", curve)
    expected = (3).to_bytes(16, 'big') + (4).to_bytes(16, 'big')
    assert res == expected

# forward der_sig input to decode_dss_signature check
def test_der_to_raw_signature_forwards_der_sig(monkeypatch):
    curve = SimpleNamespace(key_size=192)

    seen = {}

    def fake_decode(der_sig):
        seen['der_sig'] = der_sig
        return (9, 10)

    def fake_number_to_bytes(val, length):
        return int(val).to_bytes(length, 'big')

    monkeypatch.setattr(utils_module, 'decode_dss_signature', fake_decode)
    monkeypatch.setattr(utils_module, 'number_to_bytes', fake_number_to_bytes)

    der = b"abc"
    res = der_to_raw_signature(der, curve)
    assert seen.get('der_sig') == der
    expected = (9).to_bytes(24, 'big') + (10).to_bytes(24, 'big')
    assert res == expected

# large key size (512-bit) to check length calculation and concatenation
def test_der_to_raw_signature_large_key_size_512(monkeypatch):
    curve = SimpleNamespace(key_size=512)

    def fake_decode(der_sig):
        return (123456789, 987654321)

    def fake_number_to_bytes(val, length):
        return int(val).to_bytes(length, 'big')

    monkeypatch.setattr(utils_module, 'decode_dss_signature', fake_decode)
    monkeypatch.setattr(utils_module, 'number_to_bytes', fake_number_to_bytes)

    res = der_to_raw_signature(b"der-512", curve)
    expected = (123456789).to_bytes(64, 'big') + (987654321).to_bytes(64, 'big')
    assert res == expected
