from app.infrastructure.password_hasher import Argon2PasswordHasher


def test_argon2_adapter_verifies_matching_and_nonmatching_passwords() -> None:
    adapter = Argon2PasswordHasher()
    password_hash = adapter.hash("secret")
    assert adapter.verify("secret", password_hash) is True
    assert adapter.verify("wrong", password_hash) is False


def test_dummy_hash_uses_the_same_recommended_argon2_parameters() -> None:
    adapter = Argon2PasswordHasher()
    real_hash = adapter.hash("registered password")
    dummy_hash = adapter.dummy_hash()

    assert dummy_hash.split("$")[1:4] == real_hash.split("$")[1:4]
    assert adapter.verify("registered password", dummy_hash) is False
