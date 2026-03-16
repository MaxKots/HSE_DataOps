"""
users: create table
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        # ── Миграция (apply) ──────────────────────────
        """
        CREATE TABLE IF NOT EXISTS users (
            id          SERIAL PRIMARY KEY,
            username    VARCHAR(128) NOT NULL UNIQUE,
            email       VARCHAR(256) NOT NULL UNIQUE,
            created_at  TIMESTAMP WITH TIME ZONE DEFAULT now(),
            updated_at  TIMESTAMP WITH TIME ZONE DEFAULT now()
        );
        """,
        # ── Откат (rollback) ──────────────────────────
        """
        DROP TABLE IF EXISTS users;
        """
    )
]