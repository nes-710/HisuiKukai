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

    current_rank = "平"

    matched = []
    unmatched = []

    rank_words = {
        "天": "天",
        "地": "地",
        "人": "人",
        "平": "平",
        "平抜き": "平",
        "軸": "軸",
        "軸吟": "軸",
    }

    for line in text.splitlines():
        line = normalize_text(line)

        if not line:
            continue

        if line in rank_words:
            current_rank = rank_words[line]
            continue

        if line in lookup:
            item = lookup[line]
            matched.append({
                "rank": current_rank,
                "poem": item["poem"],
                "pen_name": item["pen_name"],
            })
        else:
            unmatched.append(line)

    return matched, unmatched

def create_selection_report_text(matched):

    lines = []

    for item in matched:
        lines.append(f"【{item['rank']}】")
        lines.append(item["poem"])
        lines.append(f"作者：{item['pen_name']}")
        lines.append("")

    return "\n".join(lines)