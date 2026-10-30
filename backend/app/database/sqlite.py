import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from app.config import BACKEND_DIR


DATABASE_PATH = BACKEND_DIR / "research_assistant.db"


def initialize_database() -> None:
    """
    Create the database and conversation table if they do not exist.
    """

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS conversation_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL
                    CHECK (role IN ('user', 'assistant')),
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_conversation_messages_conversation_id
            ON conversation_messages (conversation_id, id)
            """
        )


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    """
    Open a database connection and close it after use.
    Automatically commit successful transactions and roll back failures.
    """

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    try:
        yield connection
        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# Ensure the database and table exist when this module is imported.
initialize_database()