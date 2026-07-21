import base64
import binascii
from datetime import timedelta
import re
from uuid import UUID

import jwt

from app.application.errors import InvalidAccessToken
from app.application.ports.clock import Clock


ISSUER = "portal-convocatorias-api"
AUDIENCE = "portal-convocatorias-web"
TTL_SECONDS = 1800
LEEWAY_SECONDS = 30


def decode_secret(encoded: str) -> bytes:
    if not encoded:
        raise ValueError("JWT_SECRET is required")
    if re.fullmatch(r"[A-Za-z0-9_-]+={0,2}", encoded) is None:
        raise ValueError("JWT_SECRET must be base64url")
    try:
        padding = "=" * (-len(encoded) % 4)
        secret = base64.b64decode(encoded + padding, altchars=b"-_", validate=True)
    except (ValueError, binascii.Error):
        raise ValueError("JWT_SECRET must be base64url") from None
    if len(secret) < 32:
        raise ValueError("JWT_SECRET must decode to at least 32 bytes")
    return secret


class JwtAccessTokenService:
    def __init__(self, secret: bytes, clock: Clock) -> None:
        self._secret = secret
        self._clock = clock

    def issue(self, subject: str) -> str:
        parsed = UUID(subject)
        if parsed.version != 4:
            raise ValueError("JWT subject must be a UUID4")
        issued_at = self._clock.now()
        return jwt.encode(
            {
                "sub": subject,
                "iss": ISSUER,
                "aud": AUDIENCE,
                "iat": int(issued_at.timestamp()),
                "exp": int((issued_at + timedelta(seconds=TTL_SECONDS)).timestamp()),
            },
            self._secret,
            algorithm="HS256",
        )

    def verify(self, token: str) -> str:
        try:
            claims = jwt.decode(
                token,
                self._secret,
                algorithms=["HS256"],
                issuer=ISSUER,
                audience=AUDIENCE,
                options={
                    "require": ["sub", "iss", "aud", "iat", "exp"],
                    "verify_exp": False,
                    "verify_iat": False,
                },
            )
            subject = claims["sub"]
            issuer = claims["iss"]
            audience = claims["aud"]
            issued_at = claims["iat"]
            expires_at = claims["exp"]
            if (
                type(subject) is not str
                or type(issuer) is not str
                or type(audience) is not str
                or type(issued_at) is not int
                or type(expires_at) is not int
                or issuer != ISSUER
                or audience != AUDIENCE
                or expires_at - issued_at != TTL_SECONDS
            ):
                raise ValueError
            now = int(self._clock.now().timestamp())
            if issued_at > now + LEEWAY_SECONDS or now > expires_at + LEEWAY_SECONDS:
                raise ValueError
            parsed = UUID(subject)
            if parsed.version != 4:
                raise ValueError
        except (jwt.PyJWTError, KeyError, TypeError, ValueError):
            raise InvalidAccessToken from None
        return subject