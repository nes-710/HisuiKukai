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

    cursor = conn.execute(
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

    contest_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return contest_id

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

def get_status_label(status):

    labels = {
        "created": "作成済み",
        "accepting": "投句受付中",
        "closed": "投句締切",
        "selection": "選句受付中",
        "finished": "終了",
    }

    return labels.get(status, status)