from flask import Flask, render_template, request
from services.contest_service import (
    create_contest,
    get_all_contests,
    get_contest,
    get_status_label,
)
from services.submission_service import create_submission, count_participants

app = Flask(__name__)


@app.route("/")
def index():

    contests = get_all_contests()

    return render_template(
        "index.html",
        contests=contests
    )


@app.route("/create", methods=["GET", "POST"])
def create():

    if request.method == "POST":
        contest_no = request.form["contest_no"]

        theme1 = request.form["theme1"]
        judge1 = request.form["judge1"]

        theme2 = request.form["theme2"]
        judge2 = request.form["judge2"]

        free_judge = request.form["free_judge"]

        create_contest(
            contest_no,
            theme1,
            judge1,
            theme2,
            judge2,
            free_judge,
        )

        return "保存しました！"

    return render_template("create.html")

@app.route("/contest/<int:contest_id>")
def contest(contest_id):

    contest = get_contest(contest_id)

    status_label = get_status_label(contest["status"])
    participant_count = count_participants(contest_id)

    return render_template(
        "contest.html",
        contest=contest,
        status_label=status_label,
        participant_count=participant_count,
    )

@app.route("/contest/<int:contest_id>/submit", methods=["GET", "POST"])
def submit(contest_id):

    contest = get_contest(contest_id)

    if request.method == "POST":

        pen_name = request.form["pen_name"]
        pen_name_kana = request.form["pen_name_kana"]

        poems = [
            {"theme": "theme1", "text": request.form["theme1_poem1"]},
            {"theme": "theme1", "text": request.form["theme1_poem2"]},
            {"theme": "theme1", "text": request.form["theme1_poem3"]},

            {"theme": "theme2", "text": request.form["theme2_poem1"]},
            {"theme": "theme2", "text": request.form["theme2_poem2"]},
            {"theme": "theme2", "text": request.form["theme2_poem3"]},

            {"theme": "free", "text": request.form["free_poem1"]},
            {"theme": "free", "text": request.form["free_poem2"]},
            {"theme": "free", "text": request.form["free_poem3"]},
        ]

        create_submission(
            contest_id,
            pen_name,
            pen_name_kana,
            poems,
        )

        return "投句を受け付けました。"

    return render_template(
        "submit.html",
        contest=contest,
    )

if __name__ == "__main__":
    app.run(debug=True)