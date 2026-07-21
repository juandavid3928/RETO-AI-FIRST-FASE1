from collections.abc import Callable

import psycopg
from psycopg.errors import UniqueViolation

from app.application.errors import DatabaseUnavailable, DuplicateEmail
from app.domain.user import User


class PostgresUserRepository:
    def __init__(
        self,
        database_url: str,
        connect: Callable[..., psycopg.Connection] = psycopg.connect,
    ) -> None:
        self._database_url = database_url
        self._connect = connect

    def add(self, user: User) -> User:
        connection: psycopg.Connection | None = None
        try:
            connection = self._connect(self._database_url)
            connection.execute(
                """
                INSERT INTO users (id, email, password_hash, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    user.id.value,
                    user.email.value,
                    user.password_hash,
                    user.created_at,
                    user.updated_at,
                ),
            )
            connection.commit()
            return user
        except UniqueViolation as error:
            if connection is not None:
                connection.rollback()
            if error.diag.constraint_name == "uq_users_email_canonical":
                raise DuplicateEmail from None
            raise
        except psycopg.OperationalError:
            if connection is not None:
                connection.rollback()
            raise DatabaseUnavailable from None
        except Exception:
            if connection is not None:
                connection.rollback()
            raise
        finally:
            if connection is not None:
                connection.close()
