from datetime import UTC, date, datetime, timedelta, timezone
from uuid import uuid4

from app.domain.user import UserId


class SystemClock:
    def now(self) -> datetime:
        return datetime.now(tz=UTC)


class Uuid4Generator:
    def new(self) -> UserId:
        return UserId(uuid4())


class ColombiaDateProvider:
    def today_colombia(self) -> date:
        return datetime.now(tz=timezone(timedelta(hours=-5))).date()
