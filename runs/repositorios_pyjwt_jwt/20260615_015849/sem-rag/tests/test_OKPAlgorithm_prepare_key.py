from repositorios.pyjwt.jwt.algorithms import OKPAlgorithm

# teste happy path: não é str/bytes recebe o key tal como está após checagem
def test_prepare_key_non_string_object_passes_through_and_checks(monkeypatch):
    alg = OKPAlgorithm()
    sentinel = object()
    captured = {}

    def fake_check_crypto_key_type(k):
        captured["arg"] = k

    monkeypatch.setattr(alg, "check_crypto_key_type", fake_check_crypto_key_type)
    result = alg.prepare_key(sentinel)

    assert result is sentinel
    assert captured["arg"] is sentinel

# teste branch pública PEM: conteúdo começa com "-----BEGIN PUBLIC"
def test_prepare_key_public_pem_path_loads_public_key(monkeypatch):
    alg = OKPAlgorithm()
    loaded = object()

    monkeypatch.setattr(
        "repositorios.pyjwt.jwt.algorithms.load_pem_public_key",
        lambda data: loaded,
    )
    captured = {}
    monkeypatch.setattr(alg, "check_crypto_key_type", lambda k: captured.update({"arg": k}))

    pem_public_bytes = b"-----BEGIN PUBLIC KEY-----\nMIIBIj..."  # conteúdo simbólico
    result = alg.prepare_key(pem_public_bytes)

    assert result is loaded
    assert captured["arg"] is loaded

# teste branch privada PEM: conteúdo começa com "-----BEGIN PRIVATE"
def test_prepare_key_private_pem_path_loads_private_key(monkeypatch):
    alg = OKPAlgorithm()
    loaded = object()

    monkeypatch.setattr(
        "repositorios.pyjwt.jwt.algorithms.load_pem_private_key",
        lambda data, password=None: loaded,
    )
    captured = {}
    monkeypatch.setattr(alg, "check_crypto_key_type", lambda k: captured.update({"arg": k}))

    pem_private_bytes = b"-----BEGIN PRIVATE KEY-----\nMIIEvA..."  # conteúdo simbólico
    result = alg.prepare_key(pem_private_bytes)

    assert result is loaded
    assert captured["arg"] is loaded

# teste branch SSH openSSH: início da string começa com "ssh-"
def test_prepare_key_ssh_path_loads_ssh_public_key(monkeypatch):
    alg = OKPAlgorithm()
    loaded = object()

    monkeypatch.setattr(
        "repositorios.pyjwt.jwt.algorithms.load_ssh_public_key",
        lambda data: loaded,
    )
    captured = {}
    monkeypatch.setattr(alg, "check_crypto_key_type", lambda k: captured.update({"arg": k}))

    ssh_key_str = "ssh-ed25519 AAAAB3NzaC1yc2EAAAADAQABAAAABAQ"  # conteúdo simbólico
    result = alg.prepare_key(ssh_key_str)

    assert result is loaded
    assert captured["arg"] is loaded
