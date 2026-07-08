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

def shuffled_copy(poems):
    copied = poems.copy()
    random.shuffle(copied)
    return copied


def get_judge_eiso_texts(contest, grouped_eiso):

    judge_texts = []

    judge_texts.append({
        "judge": contest["judge1"],
        "theme_title": contest["theme1"],
        "text": create_eiso_text(
            contest["theme1"],
            shuffled_copy(grouped_eiso["theme1"]),
        ),
    })

    judge_texts.append({
        "judge": contest["judge2"],
        "theme_title": contest["theme2"],
        "text": create_eiso_text(
            contest["theme2"],
            shuffled_copy(grouped_eiso["theme2"]),
        ),
    })

    judge_texts.append({
        "judge": contest["free_judge"],
        "theme_title": "雑詠",
        "text": create_eiso_text(
            "雑詠",
            shuffled_copy(grouped_eiso["free"]),
        ),
    })

    judge_texts.append({
        "judge": "nes",
        "theme_title": "雑詠",
        "text": create_eiso_text(
            "雑詠",
            shuffled_copy(grouped_eiso["free"]),
        ),
    })

    return judge_texts