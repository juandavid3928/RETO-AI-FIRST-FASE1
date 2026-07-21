from typing import Protocol

from app.domain.user import User


class UserRepository(Protocol):
    def add(self, user: User) -> User: ...
