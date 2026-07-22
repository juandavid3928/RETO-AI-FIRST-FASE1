from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.application.errors import AuthenticatedUserNotFound
from app.application.ports.user_repository import UserRepository
from app.application.use_cases.validate_access_token import AuthenticatedPrincipal
from app.domain.user import UserId


@dataclass(frozen=True, slots=True)
class OwnProfile:
    id: UUID
    email: str
    created_at: datetime


class GetOwnProfile:
    def __init__(self, users: UserRepository) -> None:
        self._users = users

    def execute(self, principal: AuthenticatedPrincipal) -> OwnProfile:
        user = self._users.get_by_id(UserId(principal.user_id))
        if user is None:
            raise AuthenticatedUserNotFound
        return OwnProfile(user.id.value, user.email.value, user.created_at)
