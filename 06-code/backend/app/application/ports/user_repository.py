from typing import Protocol

from app.domain.user import User, UserId


class UserRepository(Protocol):
    def add(self, user: User) -> User: ...

    def get_by_email(self, email: str) -> User | None: ...

    def get_by_id(self, user_id: UserId) -> User | None: ...
