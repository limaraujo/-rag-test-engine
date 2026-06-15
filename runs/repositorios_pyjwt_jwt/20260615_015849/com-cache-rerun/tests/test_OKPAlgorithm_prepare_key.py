import pytest
import importlib
from repositorios.pyjwt.jwt.algorithms import OKPAlgorithm

# Import the target module and symbols
algorithms = importlib.import_module("repositorios.pyjwt.jwt.algorithms")
OKPAlgorithm = algorithms.OKPAlgorithm
InvalidKeyError = algorithms.InvalidKeyError


# Initialize: bypass __init__ to create a lightweight instance for testing
def _make_alg(monkeypatch):
    monkeypatch.setattr(OKPAlgorithm, "__init__", lambda self: None, raising=True)
    return OKPAlgorithm()


# test: non-str/bytes input should go through check_crypto_key_type and be returned unchanged
# short: happy path for non-string/non-bytes input
def test_prepare_key_non_str_calls_check_and_returns_input(monkeypatch):
    alg = _make_alg(monkeypatch)

    # capture what is passed to check_crypto_key_type
    seen = []
    def fake_check(self, val):
        seen.append(val)

    monkeypatch.setattr(OKPAlgorithm, "check_crypto_key_type", fake_check, raising=True)

    dummy_obj = object()
    res = alg.prepare_key(dummy_obj)

    assert res is dummy_obj
    assert seen == [dummy_obj]


# test: branches for public/private/ssh keys and an invalid input (4 branches total)
@pytest.mark.parametrize("case", [
    {"name": "PUBLIC", "input": "-----BEGIN PUBLIC KEY-----\nMIIB", "loader": "load_pem_public_key", "sentinel": object(), "expect_exception": False},
    {"name": "PRIVATE", "input": "-----BEGIN PRIVATE KEY-----\nMIIE", "loader": "load_pem_private_key", "sentinel": object(), "expect_exception": False},
    {"name": "SSH", "input": "ssh-ed25519 AABBCC", "loader": "load_ssh_public_key", "sentinel": object(), "expect_exception": False},
    {"name": "INVALID", "input": "not-a-key", "loader": None, "sentinel": None, "expect_exception": True},
])
def test_prepare_key_branches_branches_coverage(monkeypatch, case):
    alg = _make_alg(monkeypatch)

    # capture what is passed to check_crypto_key_type
    seen = []
    def fake_check(self, val):
        seen.append(val)

    monkeypatch.setattr(OKPAlgorithm, "check_crypto_key_type", fake_check, raising=True)

    if case["expect_exception"]:
        with pytest.raises(InvalidKeyError):
            alg.prepare_key(case["input"])
        return

    # Patch the appropriate loader to return a sentinel object
    sentinel = case["sentinel"]

    if case["name"] == "PUBLIC":
        # define a safe fake loader that accepts any kwargs
        def fake_load_pem_public_key(b, *args, **kwargs):
            return sentinel
        monkeypatch.setattr(algorithms, "load_pem_public_key", fake_load_pem_public_key, raising=True)
    elif case["name"] == "PRIVATE":
        def fake_load_pem_private_key(b, password=None, *args, **kwargs):
            return sentinel
        monkeypatch.setattr(algorithms, "load_pem_private_key", fake_load_pem_private_key, raising=True)
    elif case["name"] == "SSH":
        def fake_load_ssh_public_key(b, *args, **kwargs):
            return sentinel
        monkeypatch.setattr(algorithms, "load_ssh_public_key", fake_load_ssh_public_key, raising=True)

    res = alg.prepare_key(case["input"])

    assert res is sentinel
    assert seen == [sentinel]
