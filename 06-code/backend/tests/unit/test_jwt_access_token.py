import base64
from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt
import pytest

from app.application.errors import InvalidAccessToken
from app.application.use_cases.validate_access_token import AuthenticatedPrincipal, ValidateAccessToken
from app.infrastructure.jwt_access_token import JwtAccessTokenService, decode_secret


SECRET_BYTES = b"0123456789abcdef0123456789abcdef"
SECRET = base64.urlsafe_b64encode(SECRET_BYTES).decode().rstrip("=")
NOW = datetime.now(UTC).replace(microsecond=0)
SUBJECT = "8bb45e10-84cb-4b89-8f75-c27bbb319fe8"


class FixedClock:
    def now(self) -> datetime:
        return NOW


def test_secret_must_be_valid_base64url_with_at_least_32_decoded_bytes() -> None:
    assert decode_secret(SECRET) == SECRET_BYTES
    standard_base64 = base64.b64encode(b"\xfb" * 32).decode().rstrip("=")
    for invalid in ("", "not base64!", standard_base64, base64.urlsafe_b64encode(b"short").decode()):
        with pytest.raises(ValueError):
            decode_secret(invalid)


def test_issued_jwt_has_fixed_algorithm_and_required_claims() -> None:
    service = JwtAccessTokenService(SECRET_BYTES, FixedClock())

    token = service.issue(SUBJECT)

    assert jwt.get_unverified_header(token)["alg"] == "HS256"
    claims = jwt.decode(
        token,
        SECRET_BYTES,
        algorithms=["HS256"],
        issuer="portal-convocatorias-api",
        audience="portal-convocatorias-web",
    )
    assert claims == {
        "sub": SUBJECT,
        "iss": "portal-convocatorias-api",
        "aud": "portal-convocatorias-web",
        "iat": int(NOW.timestamp()),
        "exp": int((NOW + timedelta(seconds=1800)).timestamp()),
    }


@pytest.mark.parametrize("subject", ["not-a-uuid", "6ba7b810-9dad-11d1-80b4-00c04fd430c8"])
def test_issuer_rejects_a_subject_that_is_not_uuid4(subject: str) -> None:
    with pytest.raises((ValueError, TypeError)):
        JwtAccessTokenService(SECRET_BYTES, FixedClock()).issue(subject)


def test_verifier_accepts_valid_token_and_returns_subject() -> None:
    service = JwtAccessTokenService(SECRET_BYTES, FixedClock())
    assert service.verify(service.issue(SUBJECT)) == SUBJECT


def valid_claims() -> dict[str, object]:
    return {
        "sub": SUBJECT,
        "iss": "portal-convocatorias-api",
        "aud": "portal-convocatorias-web",
        "iat": int(NOW.timestamp()),
        "exp": int((NOW + timedelta(seconds=1800)).timestamp()),
    }


def test_verifier_rejects_a_tampered_signature() -> None:
    token = JwtAccessTokenService(SECRET_BYTES, FixedClock()).issue(SUBJECT)
    header, payload, signature = token.split(".")
    tampered_payload = f"{'A' if payload[0] != 'A' else 'B'}{payload[1:]}"
    tampered = f"{header}.{tampered_payload}.{signature}"

    with pytest.raises(InvalidAccessToken):
        JwtAccessTokenService(SECRET_BYTES, FixedClock()).verify(tampered)


@pytest.mark.parametrize("algorithm", ["none", "HS384"])
def test_verifier_rejects_none_and_non_allowlisted_algorithms(algorithm: str) -> None:
    key = None if algorithm == "none" else b"x" * 48
    token = jwt.encode(valid_claims(), key, algorithm=algorithm)

    with pytest.raises(InvalidAccessToken):
        JwtAccessTokenService(SECRET_BYTES, FixedClock()).verify(token)


@pytest.mark.parametrize("missing", ["sub", "iss", "aud", "iat", "exp"])
def test_verifier_rejects_each_missing_required_claim(missing: str) -> None:
    claims = valid_claims()
    del claims[missing]
    token = jwt.encode(claims, SECRET_BYTES, algorithm="HS256")

    with pytest.raises(InvalidAccessToken):
        JwtAccessTokenService(SECRET_BYTES, FixedClock()).verify(token)


def test_verifier_rejects_iat_more_than_30_seconds_in_the_future() -> None:
    claims = valid_claims()
    claims["iat"] = int((NOW + timedelta(seconds=31)).timestamp())
    token = jwt.encode(claims, SECRET_BYTES, algorithm="HS256")

    with pytest.raises(InvalidAccessToken):
        JwtAccessTokenService(SECRET_BYTES, FixedClock()).verify(token)


@pytest.mark.parametrize(
    "mutation",
    [
        {"aud": ["portal-convocatorias-web"]},
        {"exp": int((NOW + timedelta(hours=24)).timestamp())},
        {"exp": int((NOW - timedelta(seconds=1)).timestamp())},
    ],
)
def test_verifier_rejects_wrong_claim_types_and_non_contract_time_windows(mutation: dict[str, object]) -> None:
    claims = valid_claims() | mutation
    token = jwt.encode(claims, SECRET_BYTES, algorithm="HS256")

    with pytest.raises(InvalidAccessToken):
        JwtAccessTokenService(SECRET_BYTES, FixedClock()).verify(token)


@pytest.mark.parametrize(
    "claims",
    [
        {"sub": SUBJECT, "iss": "wrong", "aud": "portal-convocatorias-web"},
        {"sub": SUBJECT, "iss": "portal-convocatorias-api", "aud": "wrong"},
        {"sub": "not-a-uuid", "iss": "portal-convocatorias-api", "aud": "portal-convocatorias-web"},
    ],
)
def test_verifier_rejects_wrong_identity_claims(claims: dict[str, str]) -> None:
    claims |= {"iat": NOW, "exp": NOW + timedelta(seconds=1800)}
    token = jwt.encode(claims, SECRET_BYTES, algorithm="HS256")
    with pytest.raises(InvalidAccessToken):
        JwtAccessTokenService(SECRET_BYTES, FixedClock()).verify(token)


def test_verifier_rejects_token_expired_beyond_30_second_leeway() -> None:
    claims = {
        "sub": SUBJECT,
        "iss": "portal-convocatorias-api",
        "aud": "portal-convocatorias-web",
        "iat": NOW - timedelta(hours=1),
        "exp": NOW - timedelta(seconds=31),
    }
    token = jwt.encode(claims, SECRET_BYTES, algorithm="HS256")
    with pytest.raises(InvalidAccessToken):
        JwtAccessTokenService(SECRET_BYTES, FixedClock()).verify(token)


def test_verifier_uses_the_injected_clock_for_expiration() -> None:
    class ExpiredClock:
        def now(self) -> datetime:
            return NOW + timedelta(seconds=1831)

    token = JwtAccessTokenService(SECRET_BYTES, FixedClock()).issue(SUBJECT)

    with pytest.raises(InvalidAccessToken):
        JwtAccessTokenService(SECRET_BYTES, ExpiredClock()).verify(token)


@pytest.mark.parametrize("claim", ["iat", "exp"])
def test_verifier_rejects_non_integer_time_claims(claim: str) -> None:
    claims: dict[str, object] = {
        "sub": SUBJECT,
        "iss": "portal-convocatorias-api",
        "aud": "portal-convocatorias-web",
        "iat": int(NOW.timestamp()),
        "exp": int((NOW + timedelta(seconds=1800)).timestamp()),
    }
    claims[claim] = str(claims[claim])
    token = jwt.encode(claims, SECRET_BYTES, algorithm="HS256")

    with pytest.raises(InvalidAccessToken):
        JwtAccessTokenService(SECRET_BYTES, FixedClock()).verify(token)


def test_validate_access_token_builds_typed_principal() -> None:
    class Verifier:
        def verify(self, token: str) -> str:
            assert token == "jwt"
            return SUBJECT

    assert ValidateAccessToken(Verifier()).execute("jwt") == AuthenticatedPrincipal(UUID(SUBJECT))
