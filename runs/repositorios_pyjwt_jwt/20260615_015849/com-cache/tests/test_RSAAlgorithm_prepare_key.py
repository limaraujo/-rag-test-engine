import pytest
import repositorios.pyjwt.jwt.algorithms as alg
from cryptography.hazmat.primitives import hashes
from repositorios.pyjwt.jwt.algorithms import RSAAlgorithm


# Short: happy path where key is already a crypto type and should be returned unchanged
def test_prepare_key_returns_input_when_key_already_crypto_type(monkeypatch):
    algo = RSAAlgorithm(hash_alg=hashes.SHA256())
    # Ensure the first branch is taken by making _crypto_key_types include bytes
    monkeypatch.setattr(algo, "_crypto_key_types", (bytes,), raising=False)
    key = b"existing-crypto-key"
    result = algo.prepare_key(key)
    assert result is key


# Short: invalid input type should raise TypeError
def test_prepare_key_invalid_input_type_raises_type_error(monkeypatch):
    algo = RSAAlgorithm(hash_alg=hashes.SHA256())
    # Avoid triggering the first branch; key will be of unsupported type
    monkeypatch.setattr(algo, "_crypto_key_types", (bytes, str), raising=False)
    key = 12345  # not bytes or str
    with pytest.raises(TypeError):
        algo.prepare_key(key)


# Short: SSH public key path should use load_ssh_public_key and return its result
def test_prepare_key_ssh_public_key_path(monkeypatch):
    algo = RSAAlgorithm(hash_alg=hashes.SHA256())
    # Ensure bytes type does not match _crypto_key_types to proceed with PEM/SSH path
    monkeypatch.setattr(algo, "_crypto_key_types", (int,), raising=False)

    dummy_public_key = object()
    captured = {}

    def fake_load_ssh_public_key(b, *args, **kwargs):
        captured['bytes'] = b
        return dummy_public_key

    def fake_check_crypto_key_type(pk):
        captured['pk'] = pk

    # Patch module-level function used in the implementation
    monkeypatch.setattr(alg, "load_ssh_public_key", fake_load_ssh_public_key)
    monkeypatch.setattr(algo, "check_crypto_key_type", fake_check_crypto_key_type, raising=False)

    key = b"ssh-rsa AAAAB3NzaC1yc2E..."
    result = algo.prepare_key(key)

    assert result is dummy_public_key
    assert captured['bytes'] is key
    assert captured['pk'] is dummy_public_key


# Short: malformed input should lead to InvalidKeyError via nested parsing failure
def test_prepare_key_parse_failure_raises_InvalidKeyError(monkeypatch):
    algo = RSAAlgorithm(hash_alg=hashes.SHA256())
    # Avoid first-branch by not using a crypto-type instance for the key
    monkeypatch.setattr(algo, "_crypto_key_types", (int,), raising=False)

    def fake_load_pem_private_key(b, password=None):
        raise ValueError()

    def fake_load_pem_public_key(b):
        raise ValueError()

    monkeypatch.setattr(alg, "load_pem_private_key", fake_load_pem_private_key)
    monkeypatch.setattr(alg, "load_pem_public_key", fake_load_pem_public_key)

    key = b"not-a-valid-key-format"

    with pytest.raises(Exception) as excinfo:
        algo.prepare_key(key)

    assert excinfo.value.__class__.__name__ == "InvalidKeyError"
