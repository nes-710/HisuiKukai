from database import get_connection


def create_contest(
    contest_no,
    theme1,
    judge1,
    theme2,
    judge2,
    free_judge,
    deadline_at,
):

    conn = get_connection()

    cursor = conn.execute(
        """
        INSERT INTO contests
        (contest_no, theme1, judge1, theme2, judge2, free_judge, deadline_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            contest_no,
            theme1,
            judge1,
            theme2,
            judge2,
            free_judge,
            deadline_at,
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

def update_contest_status(contest_id, status):

    conn = get_connection()

    conn.execute(
        """
        UPDATE contests
        SET status = ?
        WHERE id = ?
        """,
        (status, contest_id),
    )

    conn.commit()
    conn.close()


def delete_contest(contest_id):

    conn = get_connection()

    conn.execute(
        """
        DELETE FROM submissions
        WHERE participant_id IN (
            SELECT id FROM participants
            WHERE contest_id = ?
        )
        """,
        (contest_id,),
    )

    conn.execute(
        """
        DELETE FROM participants
        WHERE contest_id = ?
        """,
        (contest_id,),
    )

    conn.execute(
        """
        DELETE FROM contests
        WHERE id = ?
        """,
        (contest_id,),
    )

    conn.commit()
    conn.close()