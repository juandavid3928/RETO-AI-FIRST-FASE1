"""Create the HU-001 users table."""

from alembic import op


revision = "20260721_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE users (
            id UUID PRIMARY KEY,
            email VARCHAR(320) NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMPTZ NOT NULL,
            updated_at TIMESTAMPTZ NOT NULL,
            CONSTRAINT uq_users_email_canonical UNIQUE (email),
            CONSTRAINT ck_users_email_canonical CHECK (email = lower(btrim(email)))
        )
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE users")
