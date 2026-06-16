import pytest
import repositorios.pyjwt.jwt.algorithms as algorithms
from repositorios.pyjwt.jwt.algorithms import OKPAlgorithm

# teste: branch não-string/bytes - verifica que check_crypto_key_type é chamado e a key original é retornada
def test_prepare_key_non_string_calls_check_and_returns_input(monkeypatch):
    captured = {}

    def dummy_check(self, key):
        captured["key"] = key

    monkeypatch.setattr(algorithms.OKPAlgorithm, "check_crypto_key_type", dummy_check, raising=True)
    inst = algorithms.OKPAlgorithm()
    some_obj = object()
    result = inst.prepare_key(some_obj)

    assert result is some_obj
    assert captured["key"] is some_obj

# teste: branch PEM público - verifica load_pem_public_key e retorno/checagem de key
def test_prepare_key_public_pem_branch(monkeypatch):
    monkeypatch.setattr(algorithms, "load_pem_public_key", lambda key_bytes: "PUBKEY_OBJ", raising=True)

    captured = {}
    def dummy_check(self, key):
        captured["key"] = key

    monkeypatch.setattr(algorithms.OKPAlgorithm, "check_crypto_key_type", dummy_check, raising=True)
    inst = algorithms.OKPAlgorithm()
    pem_public = b"-----BEGIN PUBLIC KEY-----\n---KEY---\n-----END PUBLIC KEY-----\n"
    result = inst.prepare_key(pem_public)

    assert result == "PUBKEY_OBJ"
    assert captured["key"] == "PUBKEY_OBJ"

# teste: branch PEM privado - verifica load_pem_private_key e retorno/checagem de key
def test_prepare_key_private_pem_branch(monkeypatch):
    monkeypatch.setattr(algorithms, "load_pem_private_key", lambda key_bytes, password=None: "PRIVKEY_OBJ", raising=True)

    captured = {}
    def dummy_check(self, key):
        captured["key"] = key

    monkeypatch.setattr(algorithms.OKPAlgorithm, "check_crypto_key_type", dummy_check, raising=True)
    inst = algorithms.OKPAlgorithm()
    pem_private = b"-----BEGIN PRIVATE KEY-----\n---KEY---\n-----END PRIVATE KEY-----\n"
    result = inst.prepare_key(pem_private)

    assert result == "PRIVKEY_OBJ"
    assert captured["key"] == "PRIVKEY_OBJ"

# teste: branch SSH - verifica load_ssh_public_key e retorno/checagem de key
def test_prepare_key_ssh_branch(monkeypatch):
    monkeypatch.setattr(algorithms, "load_ssh_public_key", lambda key_bytes: "SSHKEY_OBJ", raising=True)

    captured = {}
    def dummy_check(self, key):
        captured["key"] = key

    monkeypatch.setattr(algorithms.OKPAlgorithm, "check_crypto_key_type", dummy_check, raising=True)
    inst = algorithms.OKPAlgorithm()
    ssh_key = b"ssh-ed25519 AAAAB3NzaC1yc2EAAAADAQABAAAA"
    result = inst.prepare_key(ssh_key)

    assert result == "SSHKEY_OBJ"
    assert captured["key"] == "SSHKEY_OBJ"
