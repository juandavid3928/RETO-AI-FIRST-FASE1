from typing import Any, Protocol

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.application.errors import DatabaseUnavailable, DuplicateEmail
from app.domain.errors import InvalidEmail, InvalidPassword
from app.domain.user import User


MAX_BODY_BYTES = 4096


class RegistrationBodyLimitMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self._app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if (
            scope["type"] != "http"
            or scope.get("method") != "POST"
            or scope.get("path") != "/api/v1/auth/register"
        ):
            await self._app(scope, receive, send)
            return

        headers = dict(scope.get("headers", []))
        content_length = headers.get(b"content-length")
        if content_length is not None:
            try:
                declared_size = int(content_length)
            except ValueError:
                await validation_response()(scope, receive, send)
                return
            if declared_size < 0 or declared_size > MAX_BODY_BYTES:
                await validation_response()(scope, receive, send)
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
                await validation_response()(scope, receive, send)
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


class RegisterUserPort(Protocol):
    def execute(self, email: str, password: str) -> User: ...


class RegistrationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: str = Field(min_length=1, max_length=320)
    password: str = Field(min_length=12, max_length=128)

    @field_validator("email")
    @classmethod
    def trim_email(cls, value: str) -> str:
        return value.strip()


def validation_response(fields: dict[str, list[str]] | None = None) -> JSONResponse:
    error: dict[str, Any] = {
        "code": "validation_error",
        "message": "Registration data is invalid.",
    }
    if fields:
        error["fields"] = fields
    return JSONResponse(status_code=422, content={"error": error})


def create_app(*, register_user: RegisterUserPort) -> FastAPI:
    app = FastAPI(title="Portal de Convocatorias API")
    app.add_middleware(RegistrationBodyLimitMiddleware)

    @app.exception_handler(RequestValidationError)
    async def request_validation_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        fields: dict[str, list[str]] = {}
        for error in exc.errors():
            location = error.get("loc", ())
            field = str(location[-1]) if location else "body"
            fields.setdefault(field, []).append(str(error.get("msg", "Invalid value.")))
        return validation_response(fields)

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
            return validation_response({"email": ["Enter a valid email address."]})
        except InvalidPassword:
            return validation_response({"password": ["Password must contain 12 to 128 characters."]})
        except DuplicateEmail:
            return JSONResponse(
                status_code=409,
                content={
                    "error": {
                        "code": "email_already_registered",
                        "message": "Email is already registered.",
                    }
                },
            )
        except DatabaseUnavailable:
            return JSONResponse(
                status_code=503,
                content={
                    "error": {
                        "code": "database_unavailable",
                        "message": "Registration is temporarily unavailable.",
                    }
                },
            )
        return {
            "id": str(user.id),
            "email": user.email.value,
            "created_at": user.created_at.isoformat().replace("+00:00", "Z"),
        }

    return app
