from app.application.ports.clock import Clock
from app.application.ports.id_generator import IdGenerator
from app.application.ports.password_hasher import PasswordHasher
from app.application.ports.user_repository import UserRepository
from app.domain.errors import InvalidPassword
from app.domain.user import Email, User


class RegisterUser:
    def __init__(
        self,
        repository: UserRepository,
        hasher: PasswordHasher,
        clock: Clock,
        id_generator: IdGenerator,
    ) -> None:
        self._repository = repository
        self._hasher = hasher
        self._clock = clock
        self._id_generator = id_generator

    def execute(self, email: str, password: str) -> User:
        canonical_email = Email.parse(email)
        if not 12 <= len(password) <= 128:
            raise InvalidPassword

        now = self._clock.now()
        user = User(
            id=self._id_generator.new(),
            email=canonical_email,
            password_hash=self._hasher.hash(password),
            created_at=now,
            updated_at=now,
        )
        return self._repository.add(user)
