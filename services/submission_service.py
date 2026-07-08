from database import get_connection


def create_submission(contest_id, pen_name, pen_name_kana, poems):
    conn = get_connection()

    cursor = conn.execute(
        """
        INSERT INTO participants
        (contest_id, pen_name, pen_name_kana)
        VALUES (?, ?, ?)
        """,
        (contest_id, pen_name, pen_name_kana),
    )

    participant_id = cursor.lastrowid

    for poem in poems:
        conn.execute(
            """
            INSERT INTO submissions
            (participant_id, theme, poem)
            VALUES (?, ?, ?)
            """,
            (
                participant_id,
                poem["theme"],
                poem["text"],
            ),
        )

    conn.commit()
    conn.close()