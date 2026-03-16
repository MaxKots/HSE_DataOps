"""
users: add lastname column
"""

from yoyo import step

__depends__ = {"0001_users_create_table"}

steps = [
    step(
        # ── Миграция (apply) ──────────────────────────
        """
        ALTER TABLE users
            ADD COLUMN IF NOT EXISTS lastname VARCHAR(256) DEFAULT NULL;
        """,
        # ── Откат (rollback) ──────────────────────────
        """
        ALTER TABLE users
            DROP COLUMN IF EXISTS lastname;
        """
    )
]