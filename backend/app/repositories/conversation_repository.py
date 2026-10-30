from app.database.sqlite import get_connection


def save_message(
    conversation_id: str,
    role: str,
    content: str,
) -> None:
    """
    Save one message in a conversation.
    """

    if role not in {"user", "assistant"}:
        raise ValueError("Role must be 'user' or 'assistant'.")

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO conversation_messages (
                conversation_id,
                role,
                content
            )
            VALUES (?, ?, ?)
            """,
            (conversation_id, role, content),
        )


def get_conversation_history(
    conversation_id: str,
) -> list[dict]:
    """
    Retrieve messages from a conversation in chronological order.
    """

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT role, content, created_at
            FROM conversation_messages
            WHERE conversation_id = ?
            ORDER BY id ASC
            """,
            (conversation_id,),
        ).fetchall()

    return [
        {
            "role": row["role"],
            "content": row["content"],
            "created_at": row["created_at"],
        }
        for row in rows
    ]


def delete_conversation(conversation_id: str) -> int:
    """
    Delete all messages belonging to a conversation.
    Returns the number of deleted messages.
    """

    with get_connection() as connection:
        cursor = connection.execute(
            """
            DELETE FROM conversation_messages
            WHERE conversation_id = ?
            """,
            (conversation_id,),
        )

        return cursor.rowcount