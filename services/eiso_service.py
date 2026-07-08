from database import get_connection
import random
import math


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

def create_eiso_text(title, poems):

    count = len(poems)

    minimum = math.ceil(count * 0.4)
    maximum = math.floor(count * 0.5)

    lines = []

    lines.append(f'題「{title}」の投句一覧をお送りします。')
    lines.append(
        f'計{count}句あるので{minimum}～{maximum}句（40～50%）を抜いて頂ければと思います。よろしくお願いします。'
    )

    lines.append("")

    lines.extend(poems)

    return "\n".join(lines)