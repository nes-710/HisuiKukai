from database import get_connection


def get_eiso_data(contest_id):
    conn = get_connection()

    submissions = conn.execute(
        """
        SELECT
            submissions.theme,
            submissions.poem
        FROM submissions
        JOIN participants
        ON submissions.participant_id = participants.id
        WHERE participants.contest_id = ?
        ORDER BY submissions.theme, submissions.id
        """,
        (contest_id,),
    ).fetchall()

    conn.close()

    return submissions