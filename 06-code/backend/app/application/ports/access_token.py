from typing import Protocol


class AccessTokenIssuer(Protocol):
    def issue(self, subject: str) -> str: ...


class AccessTokenVerifier(Protocol):
    def verify(self, token: str) -> str: ...