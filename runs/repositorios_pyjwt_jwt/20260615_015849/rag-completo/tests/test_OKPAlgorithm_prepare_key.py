import importlib
from repositorios.pyjwt.jwt.algorithms import OKPAlgorithm

# test 1: caminho through for non-string/non-bytes input
def test_prepare_key_non_string_pass_through(monkeypatch):
    mod = importlib.import_module("repositorios.pyjwt.jwt.algorithms")
    class DummyOKPAlgorithm(mod.OKPAlgorithm):
        def __init__(self): 
            pass
        def check_crypto_key_type(self, key):
            self.checked = key
    alg = DummyOKPAlgorithm()
    sentinel = object()
    res = alg.prepare_key(sentinel)
    assert res is sentinel
    assert getattr(alg, "checked", None) is sentinel

# test 2: carregar chave pública PEM através de "BEGIN PUBLIC" path
def test_prepare_key_loads_public_pem(monkeypatch):
    mod = importlib.import_module("repositorios.pyjwt.jwt.algorithms")
    sentinel = object()
    monkeypatch.setattr(mod, "load_pem_public_key", lambda b: sentinel)
    class DummyOKPAlgorithm(mod.OKPAlgorithm):
        def __init__(self): 
            pass
        def check_crypto_key_type(self, key):
            self.checked = key
    alg = DummyOKPAlgorithm()
    key = b"-----BEGIN PUBLIC KEY-----\nMIIBIj..."
    res = alg.prepare_key(key)
    assert res is sentinel
    assert alg.checked is sentinel

# test 3: carregar chave privada PEM através de "BEGIN PRIVATE" path
def test_prepare_key_loads_private_pem(monkeypatch):
    mod = importlib.import_module("repositorios.pyjwt.jwt.algorithms")
    sentinel = object()
    monkeypatch.setattr(mod, "load_pem_private_key", lambda data, password=None: sentinel)
    class DummyOKPAlgorithm(mod.OKPAlgorithm):
        def __init__(self): 
            pass
        def check_crypto_key_type(self, key):
            self.checked = key
    alg = DummyOKPAlgorithm()
    key = "-----BEGIN PRIVATE KEY-----"
    res = alg.prepare_key(key)
    assert res is sentinel
    assert alg.checked is sentinel

# test 4: carregar chave SSH pública através de "ssh-" path
def test_prepare_key_loads_ssh_public(monkeypatch):
    mod = importlib.import_module("repositorios.pyjwt.jwt.algorithms")
    sentinel = object()
    monkeypatch.setattr(mod, "load_ssh_public_key", lambda data: sentinel)
    class DummyOKPAlgorithm(mod.OKPAlgorithm):
        def __init__(self): 
            pass
        def check_crypto_key_type(self, key):
            self.checked = key
    alg = DummyOKPAlgorithm()
    key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI..."
    res = alg.prepare_key(key)
    assert res is sentinel
    assert alg.checked is sentinel
