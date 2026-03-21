"""
predictions: create table
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
        CREATE TABLE IF NOT EXISTS prediction_logs (
            id SERIAL PRIMARY KEY,
            input_data TEXT NOT NULL,
            output DOUBLE PRECISION NOT NULL,
            model_version VARCHAR(32) NOT NULL,
            created_at TIMESTAMP DEFAULT now()
        );
        """,
        """
        DROP TABLE IF EXISTS prediction_logs;
        """
    )
]