from app.application.errors import InvalidCredentials
from app.application.ports.access_token import AccessTokenIssuer
from app.application.ports.password_verifier import PasswordVerifier
from app.application.ports.user_repository import UserRepository
from app.domain.errors import InvalidEmail
from app.domain.user import Email


class AuthenticateUser:
    def __init__(
        self,
        users: UserRepository,
        passwords: PasswordVerifier,
        tokens: AccessTokenIssuer,
        dummy_password_hash: str,
    ) -> None:
        self._users = users
        self._passwords = passwords
        self._tokens = tokens
        self._dummy_password_hash = dummy_password_hash

    def execute(self, email: str, password: str) -> str:
        try:
            canonical_email = Email.parse(email).value
        except InvalidEmail:
            raise InvalidCredentials from None
        user = self._users.get_by_email(canonical_email)
        password_hash = user.password_hash if user is not None else self._dummy_password_hash
        valid = self._passwords.verify(password, password_hash)
        if user is None or not valid:
            raise InvalidCredentials
        return self._tokens.issue(str(user.id))