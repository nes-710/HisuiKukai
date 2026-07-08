from database import get_connection


def create_contest(
    contest_no,
    theme1,
    judge1,
    theme2,
    judge2,
    free_judge,
):

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO contests
        (contest_no, theme1, judge1, theme2, judge2, free_judge)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            contest_no,
            theme1,
            judge1,
            theme2,
            judge2,
            free_judge,
        ),
    )

    conn.commit()
    conn.close()

def get_all_contests():

    conn = get_connection()

    contests = conn.execute(
        """
        SELECT *
        FROM contests
        ORDER BY created_at DESC
        """
    ).fetchall()

    conn.close()

    return contests

def get_contest(contest_id):

    conn = get_connection()

    contest = conn.execute(
        """
        SELECT *
        FROM contests
        WHERE id = ?
        """,
        (contest_id,),
    ).fetchone()

    conn.close()

    return contest