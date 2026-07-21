from dataclasses import dataclass
from datetime import datetime
import re
from uuid import UUID

from app.domain.errors import InvalidEmail


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?\.[A-Za-z]{2,63}$")
LOCAL_PART_PATTERN = re.compile(r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+$")


@dataclass(frozen=True, slots=True)
class Email:
    value: str

    @classmethod
    def parse(cls, raw: str) -> "Email":
        canonical = raw.strip().casefold()
        local_part, separator, domain = canonical.partition("@")
        domain_labels = domain.split(".")
        invalid_structure = (
            not separator
            or not 1 <= len(local_part) <= 64
            or local_part.startswith(".")
            or local_part.endswith(".")
            or ".." in local_part
            or LOCAL_PART_PATTERN.fullmatch(local_part) is None
            or any(not label or len(label) > 63 or label.startswith("-") or label.endswith("-") for label in domain_labels)
        )
        if len(canonical) > 254 or invalid_structure or not EMAIL_PATTERN.fullmatch(canonical):
            raise InvalidEmail("Invalid email")
        return cls(canonical)


@dataclass(frozen=True, slots=True)
class UserId:
    value: UUID

    def __post_init__(self) -> None:
        if self.value.version != 4:
            raise ValueError("UserId must contain a UUID4")

    @property
    def version(self) -> int | None:
        return self.value.version

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True, slots=True)
class User:
    id: UserId
    email: Email
    password_hash: str
    created_at: datetime
    updated_at: datetime
