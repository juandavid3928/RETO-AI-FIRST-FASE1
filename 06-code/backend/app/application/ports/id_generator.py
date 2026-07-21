from typing import Protocol

from app.domain.user import UserId


class IdGenerator(Protocol):
    def new(self) -> UserId: ...
