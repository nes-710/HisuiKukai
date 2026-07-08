from database import get_connection


def normalize_text(text):
    return text.strip().replace("　", " ")


def get_poem_lookup(contest_id, theme=None):
    conn = get_connection()

    sql = """
        SELECT
            submissions.poem,
            submissions.theme,
            participants.pen_name
        FROM submissions
        JOIN participants
        ON submissions.participant_id = participants.id
        WHERE participants.contest_id = ?
    """

    params = [contest_id]

    if theme:
        sql += " AND submissions.theme = ?"
        params.append(theme)

    rows = conn.execute(sql, params).fetchall()

    conn.close()

    lookup = {}

    for row in rows:
        key = normalize_text(row["poem"])
        lookup[key] = {
            "poem": row["poem"],
            "pen_name": row["pen_name"],
            "theme": row["theme"],
        }

    return lookup


def analyze_selection_text(contest_id, text, theme=None):
    lookup = get_poem_lookup(contest_id, theme)

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

        rank = item["rank"]

        if rank == "平":
            author_line = f"／{item['pen_name']}"
        else:
            author_line = f"／{item['pen_name']}（{rank}）"

        lines.append(item["poem"])
        lines.append(author_line)
        lines.append("")

    return "\n".join(lines)