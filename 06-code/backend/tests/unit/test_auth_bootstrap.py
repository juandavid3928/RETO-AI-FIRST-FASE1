import base64

import pytest

from app.bootstrap import build_app



VALID_SECRET = base64.urlsafe_b64encode(b"0123456789abcdef0123456789abcdef").decode().rstrip("=")
def test_bootstrap_requires_jwt_secret_without_a_default() -> None:
    with pytest.raises(TypeError):
        build_app("postgresql://unused")


def test_bootstrap_generates_the_dummy_hash_and_rejects_an_invalid_secret() -> None:
    assert build_app("postgresql://unused", VALID_SECRET) is not None
    with pytest.raises(ValueError):
        build_app("postgresql://unused", "short")
