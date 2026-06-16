import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from repositorios.pyjwt.jwt.algorithms import OKPAlgorithm
from cryptography.hazmat.primitives.asymmetric.ed448 import Ed448PrivateKey

import pytest

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from repositorios.pyjwt.jwt.algorithms import OKPAlgorithm

# Optional: Ed448 support might not be available in all environments
try:
    from cryptography.hazmat.primitives.asymmetric.ed448 import Ed448PrivateKey
    HAVE_ED448 = True
except Exception:
    Ed448PrivateKey = None
    HAVE_ED448 = False


# happy path: sign string input with Ed25519 private key
def test_sign_string_ed25519_happy_path():
    key = Ed25519PrivateKey.generate()
    msg = "hello world"
    signature = OKPAlgorithm.sign(None, msg, key)
    assert isinstance(signature, bytes)
    assert len(signature) == 64


# happy path: sign bytes input with Ed25519 private key
def test_sign_bytes_ed25519_happy_path():
    key = Ed25519PrivateKey.generate()
    msg = b"\x00\x01sample data"
    signature = OKPAlgorithm.sign(None, msg, key)
    assert isinstance(signature, bytes)
    assert len(signature) == 64


# happy path: sign string input with Ed448 private key (if available)
def test_sign_string_ed448_happy_path():
    if not HAVE_ED448:
        pytest.skip("Ed448 not available in this environment")
    key = Ed448PrivateKey.generate()
    msg = "hello world"
    signature = OKPAlgorithm.sign(None, msg, key)
    assert isinstance(signature, bytes)
    assert len(signature) == 114


# happy path: sign bytes input with Ed448 private key (if available)
def test_sign_bytes_ed448_happy_path():
    if not HAVE_ED448:
        pytest.skip("Ed448 not available in this environment")
    key = Ed448PrivateKey.generate()
    msg = b"\x00\x01sample data"
    signature = OKPAlgorithm.sign(None, msg, key)
    assert isinstance(signature, bytes)
    assert len(signature) == 114
