from datetime import UTC, datetime
from uuid import uuid4

from app.domain.user import UserId


class SystemClock:
    def now(self) -> datetime:
        return datetime.now(UTC)


class Uuid4Generator:
    def new(self) -> UserId:
        return UserId(uuid4())
