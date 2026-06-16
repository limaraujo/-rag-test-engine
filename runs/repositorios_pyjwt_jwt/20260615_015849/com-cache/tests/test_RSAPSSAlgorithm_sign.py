import pytest
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from repositorios.pyjwt.jwt.algorithms import RSAPSSAlgorithm


# short: happy path verify that sign delegates to key.sign with proper padding and hash
@pytest.mark.parametrize("hash_alg", [hashes.SHA256(), hashes.SHA384()])
def test_sign_uses_expected_hash_and_padding(hash_alg):
    # prepare RSAPSSAlgorithm instance without __init__
    instance = RSAPSSAlgorithm.__new__(RSAPSSAlgorithm)
    # pretend the algorithm hash is provided by a simple callable
    instance.hash_alg = lambda: hash_alg  # type: ignore[attr-defined]

    class MockKey:
        def __init__(self):
            self.called = False
            self.msg = None
            self.padding_obj = None
            self.algo = None
            self.return_sig = b"signature"

        def sign(self, msg, padding_obj, algorithm):
            self.called = True
            self.msg = msg
            self.padding_obj = padding_obj
            self.algo = algorithm
            return self.return_sig

    mock_key = MockKey()
    msg = b"test message"

    sig = instance.sign(msg, mock_key)

    assert mock_key.called
    assert mock_key.msg == msg
    assert isinstance(mock_key.padding_obj, padding.PSS)
    # MGF1 should wrap the provided hash_alg
    assert isinstance(mock_key.padding_obj.mgf, padding.MGF1)
    assert mock_key.padding_obj.mgf._algorithm is hash_alg  # type: ignore[attr-defined]

    # salt_length compatibility across cryptography versions
    salt_length = getattr(mock_key.padding_obj, "salt_length", None)
    if salt_length is None:
        salt_length = getattr(mock_key.padding_obj, "_salt_length", None)
    assert salt_length == hash_alg.digest_size  # type: ignore[attr-defined]

    # the hash algorithm passed to key.sign should be the same as hash_alg
    assert mock_key.algo is hash_alg
    assert sig == mock_key.return_sig


# short: exception propagation when the underlying key.sign raises
def test_sign_propagates_exception_from_key_sign():
    instance = RSAPSSAlgorithm.__new__(RSAPSSAlgorithm)
    instance.hash_alg = lambda: hashes.SHA256()  # type: ignore[attr-defined]

    class MockKey:
        def sign(self, msg, padding_obj, algorithm):
            raise ValueError("underlying key error")

    mock_key = MockKey()
    with pytest.raises(ValueError, match="underlying key error"):
        instance.sign(b"data", mock_key)
