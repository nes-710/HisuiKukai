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

def count_participants(contest_id):
    conn = get_connection()

    count = conn.execute(
        """
        SELECT COUNT(*) AS count
        FROM participants
        WHERE contest_id = ?
        """,
        (contest_id,),
    ).fetchone()

    conn.close()

    return count["count"]

def get_submissions(contest_id):

    conn = get_connection()

    submissions = conn.execute(
        """
        SELECT

            participants.pen_name,
            participants.pen_name_kana,

            submissions.theme,
            submissions.poem

        FROM submissions

        JOIN participants
        ON submissions.participant_id = participants.id

        WHERE participants.contest_id = ?

        ORDER BY participants.id
        """,
        (contest_id,),
    ).fetchall()

    conn.close()

    return submissions