import pytest
import importlib
from repositorios.pyjwt.jwt.utils import to_base64url_uint

# Verifica valores negativos geram ValueError (caso de borda)
def test_to_base64url_uint_negative_raises():
    mod = importlib.import_module("repositorios.pyjwt.jwt.utils")
    with pytest.raises(ValueError, match="Must be a positive integer"):
        mod.to_base64url_uint(-1)

# Verifica caminho não-vazio: bytes_from_int retorna bytes válidos; verifica forward de bit_length e retorno
def test_to_base64url_uint_nonempty_uses_bytes_from_int(monkeypatch):
    mod = importlib.import_module("repositorios.pyjwt.jwt.utils")
    captured = {}
    def fake_bytes_from_int(val, *, bit_length=None):
        captured["val"] = val
        captured["bit_length"] = bit_length
        return b"\x01\x02"
    def fake_base64url_encode(data):
        captured["encoded"] = data
        return b"ENCODED"
    monkeypatch.setattr(mod, "bytes_from_int", fake_bytes_from_int)
    monkeypatch.setattr(mod, "base64url_encode", fake_base64url_encode)
    res = mod.to_base64url_uint(258, bit_length=16)
    assert res == b"ENCODED"
    assert captured["val"] == 258
    assert captured["bit_length"] == 16
    assert captured["encoded"] == b"\x01\x02"

# Verifica caminho vazio: bytes_from_int retorna b''; deve usar b'\x00' antes de base64url_encode
def test_to_base64url_uint_empty_bytes_treated_as_zero(monkeypatch):
    mod = importlib.import_module("repositorios.pyjwt.jwt.utils")
    captured = {}
    def fake_bytes_from_int(val, *, bit_length=None):
        captured["val"] = val
        captured["bit_length"] = bit_length
        return b""
    def fake_base64url_encode(data):
        captured["encoded"] = data
        return b"ENCODED_ZERO"
    monkeypatch.setattr(mod, "bytes_from_int", fake_bytes_from_int)
    monkeypatch.setattr(mod, "base64url_encode", fake_base64url_encode)
    res = mod.to_base64url_uint(0)
    assert res == b"ENCODED_ZERO"
    assert captured["val"] == 0
    assert captured["bit_length"] is None
    assert captured["encoded"] == b"\x00"

# Verifica que bit_length padrão None é encaminhado quando não informado
def test_to_base64url_uint_default_bit_length_forwarded(monkeypatch):
    mod = importlib.import_module("repositorios.pyjwt.jwt.utils")
    captured = {}
    def fake_bytes_from_int(val, *, bit_length=None):
        captured["bit_length"] = bit_length
        return b"\x05"
    def fake_base64url_encode(data):
        captured["encoded"] = data
        return b"ENCODED"
    monkeypatch.setattr(mod, "bytes_from_int", fake_bytes_from_int)
    monkeypatch.setattr(mod, "base64url_encode", fake_base64url_encode)
    res = mod.to_base64url_uint(5)
    assert res == b"ENCODED"
    assert captured["bit_length"] is None
