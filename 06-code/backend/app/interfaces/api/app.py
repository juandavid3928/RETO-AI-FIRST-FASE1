from datetime import UTC
from typing import Any, Protocol

from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic_core import PydanticCustomError
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.application.errors import (
    AuthenticatedUserNotFound,
    DatabaseUnavailable,
    DuplicateEmail,
    InvalidAccessToken,
    InvalidCredentials,
)
from app.application.use_cases.get_own_profile import OwnProfile
from app.application.use_cases.validate_access_token import AuthenticatedPrincipal
from app.domain.errors import InvalidEmail, InvalidPassword
from app.domain.user import Email, User

MAX_BODY_BYTES = 4096
AUTH_POST_PATHS = {"/api/v1/auth/register", "/api/v1/auth/login"}


class AuthBodyLimitMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self._app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http" or scope.get("method") != "POST" or scope.get("path") not in AUTH_POST_PATHS:
            await self._app(scope, receive, send)
            return
        validation_message = (
            "Login data is invalid."
            if scope.get("path") == "/api/v1/auth/login"
            else "Registration data is invalid."
        )
        headers = dict(scope.get("headers", []))
        content_length = headers.get(b"content-length")
        if content_length is not None:
            try:
                declared_size = int(content_length)
            except ValueError:
                await validation_response(message=validation_message)(scope, receive, send)
                return
            if declared_size < 0 or declared_size > MAX_BODY_BYTES:
                await validation_response(message=validation_message)(scope, receive, send)
                return
        buffered: list[Message] = []
        total = 0
        while True:
            message = await receive()
            if message["type"] != "http.request":
                buffered.append(message)
                break
            total += len(message.get("body", b""))
            if total > MAX_BODY_BYTES:
                await validation_response(message=validation_message)(scope, receive, send)
                return
            buffered.append(message)
            if not message.get("more_body", False):
                break
        index = 0

        async def replay_receive() -> Message:
            nonlocal index
            if index < len(buffered):
                message = buffered[index]
                index += 1
                return message
            return await receive()

        await self._app(scope, replay_receive, send)


class PrivateNoStoreMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self._app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        path = scope.get("path")
        if scope["type"] != "http" or path not in {"/api/v1/auth/login", "/api/v1/users/me"}:
            await self._app(scope, receive, send)
            return

        async def add_headers(message: Message) -> None:
            if message["type"] == "http.response.start":
                private_headers = [
                    (b"cache-control", b"no-store"),
                    (b"pragma", b"no-cache"),
                ]
                if path == "/api/v1/users/me":
                    private_headers.append((b"vary", b"Authorization"))
                message["headers"] = list(message.get("headers", [])) + private_headers
            await send(message)

        await self._app(scope, receive, add_headers)


class RegisterUserPort(Protocol):
    def execute(self, email: str, password: str) -> User: ...


class AuthenticateUserPort(Protocol):
    def execute(self, email: str, password: str) -> str: ...


class ValidateAccessTokenPort(Protocol):
    def execute(self, token: str) -> AuthenticatedPrincipal: ...


class GetOwnProfilePort(Protocol):
    def execute(self, principal: AuthenticatedPrincipal) -> OwnProfile: ...


class RegistrationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: str = Field(min_length=1, max_length=320)
    password: str = Field(min_length=12, max_length=128)

    @field_validator("email")
    @classmethod
    def trim_email(cls, value: str) -> str:
        return value.strip()


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: str = Field(min_length=1, max_length=320)
    password: str = Field(min_length=1, max_length=128)

    @field_validator("email")
    @classmethod
    def trim_email(cls, value: str) -> str:
        trimmed = value.strip()
        try:
            Email.parse(trimmed)
        except InvalidEmail:
            raise PydanticCustomError("invalid_email", "Enter a valid email address.") from None
        return trimmed


def validation_response(
    fields: dict[str, list[str]] | None = None,
    *,
    message: str = "Request data is invalid.",
) -> JSONResponse:
    error: dict[str, Any] = {"code": "validation_error", "message": message}
    if fields:
        error["fields"] = fields
    return JSONResponse(status_code=422, content={"error": error})


class BearerFailure(Exception):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message


def create_app(
    *,
    register_user: RegisterUserPort,
    authenticate_user: AuthenticateUserPort | None = None,
    validate_access_token: ValidateAccessTokenPort | None = None,
    get_own_profile: GetOwnProfilePort | None = None,
) -> FastAPI:
    app = FastAPI(title="Portal de Convocatorias API")
    app.add_middleware(AuthBodyLimitMiddleware)
    app.add_middleware(PrivateNoStoreMiddleware)
    bearer = HTTPBearer(auto_error=False)

    def require_principal(
        request: Request,
        credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    ) -> AuthenticatedPrincipal:
        if credentials is None:
            if request.headers.get("authorization"):
                raise BearerFailure("invalid_token", "Access token is invalid.")
            raise BearerFailure("authentication_required", "Authentication is required.")
        if validate_access_token is None:
            raise BearerFailure("invalid_token", "Access token is invalid.")
        try:
            return validate_access_token.execute(credentials.credentials)
        except InvalidAccessToken:
            raise BearerFailure("invalid_token", "Access token is invalid.") from None

    app.state.require_principal = require_principal

    @app.exception_handler(RequestValidationError)
    async def request_validation_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        fields: dict[str, list[str]] = {}
        for error in exc.errors():
            location = error.get("loc", ())
            field = str(location[-1]) if location else "body"
            fields.setdefault(field, []).append(str(error.get("msg", "Invalid value.")))
        message = (
            "Login data is invalid."
            if request.url.path == "/api/v1/auth/login"
            else "Registration data is invalid."
        )
        return validation_response(fields, message=message)

    @app.exception_handler(BearerFailure)
    async def bearer_failure_handler(_: Request, exc: BearerFailure) -> JSONResponse:
        return JSONResponse(
            status_code=401,
            content={"error": {"code": exc.code, "message": exc.message}},
            headers={"WWW-Authenticate": "Bearer"},
        )

    @app.exception_handler(Exception)
    async def unexpected_error_handler(_: Request, __: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={"error": {"code": "internal_error", "message": "An unexpected error occurred."}},
        )

    @app.post("/api/v1/auth/register", status_code=201)
    def register(payload: RegistrationRequest) -> Any:
        try:
            user = register_user.execute(payload.email, payload.password)
        except InvalidEmail:
            return validation_response(
                {"email": ["Enter a valid email address."]},
                message="Registration data is invalid.",
            )
        except InvalidPassword:
            return validation_response(
                {"password": ["Password must contain 12 to 128 characters."]},
                message="Registration data is invalid.",
            )
        except DuplicateEmail:
            return JSONResponse(status_code=409, content={"error": {"code": "email_already_registered", "message": "Email is already registered."}})
        except DatabaseUnavailable:
            return JSONResponse(status_code=503, content={"error": {"code": "database_unavailable", "message": "Registration is temporarily unavailable."}})
        return {
            "id": str(user.id),
            "email": user.email.value,
            "created_at": user.created_at.isoformat().replace("+00:00", "Z"),
        }

    @app.post("/api/v1/auth/login")
    def login(payload: LoginRequest) -> Any:
        if authenticate_user is None:
            raise RuntimeError("Login is not configured")
        try:
            token = authenticate_user.execute(payload.email, payload.password)
        except InvalidCredentials:
            return JSONResponse(
                status_code=401,
                content={"error": {"code": "invalid_credentials", "message": "Email or password is incorrect."}},
                headers={"WWW-Authenticate": "Bearer"},
            )
        except DatabaseUnavailable:
            return JSONResponse(status_code=503, content={"error": {"code": "database_unavailable", "message": "Login is temporarily unavailable."}})
        except Exception:
            return JSONResponse(
                status_code=500,
                content={"error": {"code": "internal_error", "message": "An unexpected error occurred."}},
            )
        return {"access_token": token, "token_type": "bearer", "expires_in": 1800}

    @app.get("/api/v1/users/me")
    def own_profile(principal: AuthenticatedPrincipal = Depends(require_principal)) -> Any:
        if get_own_profile is None:
            raise RuntimeError("Own profile is not configured")
        try:
            profile = get_own_profile.execute(principal)
        except AuthenticatedUserNotFound:
            raise BearerFailure("invalid_token", "Access token is invalid.") from None
        except DatabaseUnavailable:
            return JSONResponse(
                status_code=503,
                content={"error": {"code": "database_unavailable", "message": "Profile is temporarily unavailable."}},
            )
        except Exception:
            return JSONResponse(
                status_code=500,
                content={"error": {"code": "internal_error", "message": "An unexpected error occurred."}},
            )
        return {
            "id": str(profile.id),
            "email": profile.email,
            "created_at": profile.created_at.astimezone(UTC).isoformat().replace("+00:00", "Z"),
        }

    return app
