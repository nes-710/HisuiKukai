from database import get_connection
import random


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

def group_and_shuffle_eiso(submissions):

    grouped = {
        "theme1": [],
        "theme2": [],
        "free": [],
    }

    for submission in submissions:
        grouped[submission["theme"]].append(submission["poem"])

    for theme in grouped:
        random.shuffle(grouped[theme])

    return grouped