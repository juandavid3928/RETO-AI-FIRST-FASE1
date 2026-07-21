from typing import Protocol


class PasswordVerifier(Protocol):
    def verify(self, password: str, password_hash: str) -> bool: ...