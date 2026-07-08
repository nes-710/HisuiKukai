from database import get_connection


def normalize_text(text):
    return text.strip().replace("　", " ")


def get_poem_lookup(contest_id):
    conn = get_connection()

    rows = conn.execute(
        """
        SELECT
            submissions.poem,
            participants.pen_name
        FROM submissions
        JOIN participants
        ON submissions.participant_id = participants.id
        WHERE participants.contest_id = ?
        """,
        (contest_id,),
    ).fetchall()

    conn.close()

    lookup = {}

    for row in rows:
        key = normalize_text(row["poem"])
        lookup[key] = {
            "poem": row["poem"],
            "pen_name": row["pen_name"],
        }

    return lookup


def analyze_selection_text(contest_id, text):
    lookup = get_poem_lookup(contest_id)

    matched = []
    unmatched = []

    for line in text.splitlines():
        line = normalize_text(line)

        if not line:
            continue

        if line in lookup:
            matched.append(lookup[line])
        else:
            unmatched.append(line)

    return matched, unmatched