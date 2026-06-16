import pytest
import repositorios.pyjwt.jwt.utils as utils
from repositorios.pyjwt.jwt.utils import is_ssh_key

# happy path: key starts with a valid SSH prefix; supports multiple prefixes via monkeypatch
def test_is_ssh_key_happy_path(monkeypatch):
    monkeypatch.setattr(utils, "_SSH_KEY_FORMATS", (b"ssh-ed25519 ", b"ssh-rsa "))
    assert is_ssh_key(b"ssh-ed25519 user@example.com") is True
    assert is_ssh_key(b"ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ") is True

# negative path: key does not start with any SSH prefix
def test_is_ssh_key_negative(monkeypatch):
    monkeypatch.setattr(utils, "_SSH_KEY_FORMATS", (b"ssh-ed25519 ",))
    assert is_ssh_key(b"not-a-key") is False
    assert is_ssh_key(b"SSH-KEYS") is False

# edge case: empty key returns False
def test_is_ssh_key_empty(monkeypatch):
    monkeypatch.setattr(utils, "_SSH_KEY_FORMATS", (b"ssh-ed25519 ",))
    assert is_ssh_key(b"") is False
