from dataclasses import dataclass
from uuid import UUID

from app.application.errors import InvalidAccessToken
from app.application.ports.access_token import AccessTokenVerifier


@dataclass(frozen=True, slots=True)
class AuthenticatedPrincipal:
    user_id: UUID


class ValidateAccessToken:
    def __init__(self, verifier: AccessTokenVerifier) -> None:
        self._verifier = verifier

    def execute(self, token: str) -> AuthenticatedPrincipal:
        try:
            user_id = UUID(self._verifier.verify(token))
        except (ValueError, TypeError):
            raise InvalidAccessToken from None
        if user_id.version != 4:
            raise InvalidAccessToken
        return AuthenticatedPrincipal(user_id)