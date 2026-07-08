from flask import Flask, render_template, request, redirect, url_for
from services.contest_service import (
    create_contest,
    get_all_contests,
    get_contest,
    get_status_label,
    update_contest_status,
    delete_contest,
    close_contest_if_deadline_passed,
    update_deadline,
)
from services.submission_service import (
    create_submission,
    count_participants,
    get_submissions,
)
from services.eiso_service import (
    get_eiso_data,
    group_and_shuffle_eiso,
    create_eiso_text,
    get_judge_eiso_texts,
)
from services.selection_service import (
    analyze_selection_text,
    create_selection_report_text,
)

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

        deadline_at = request.form["deadline_at"]

        contest_id = create_contest(
            contest_no,
            theme1,
            judge1,
            theme2,
            judge2,
            free_judge,
            deadline_at,
        )

        return redirect(
            url_for("contest", contest_id=contest_id)
        )

    return render_template("create.html")

@app.route("/contest/<int:contest_id>")
def contest(contest_id):

    contest = get_contest(contest_id)

    close_contest_if_deadline_passed(contest)
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

    close_contest_if_deadline_passed(contest)
    contest = get_contest(contest_id)

    if contest["status"] != "accepting":
        return render_template(
            "submit_closed.html",
            contest=contest,
        )

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

        return redirect(url_for("submit_complete", contest_id=contest_id))

    return render_template(
        "submit.html",
        contest=contest,
    )

@app.route("/contest/<int:contest_id>/submit/complete")
def submit_complete(contest_id):

    contest = get_contest(contest_id)

    return render_template(
        "submit_complete.html",
        contest=contest,
    )

@app.route("/contest/<int:contest_id>/submissions")
def submissions(contest_id):

    contest = get_contest(contest_id)

    submissions = get_submissions(contest_id)

    return render_template(
        "submissions.html",
        contest=contest,
        submissions=submissions,
    )

@app.route("/contest/<int:contest_id>/eiso")
def eiso(contest_id):

    contest = get_contest(contest_id)
    submissions = get_eiso_data(contest_id)
    grouped_eiso = group_and_shuffle_eiso(submissions)

    theme1_text = create_eiso_text(
        contest["theme1"],
        grouped_eiso["theme1"],
    )

    theme2_text = create_eiso_text(
        contest["theme2"],
        grouped_eiso["theme2"],
    )

    free_text = create_eiso_text(
        "雑詠",
        grouped_eiso["free"],
    )

    judge_eiso_texts = get_judge_eiso_texts(
        contest,
        grouped_eiso,
    )

    return render_template(
        "eiso.html",
        contest=contest,
        grouped_eiso=grouped_eiso,
        theme1_text=theme1_text,
        theme2_text=theme2_text,
        free_text=free_text,
        judge_eiso_texts=judge_eiso_texts,
    )

@app.route("/contest/<int:contest_id>/selection", methods=["GET", "POST"])
def selection(contest_id):
    selected_theme = "theme1"
    report_text = ""
    contest = get_contest(contest_id)

    matched = []
    unmatched = []
    raw_text = ""

    if request.method == "POST":
        raw_text = request.form["selection_text"]
        selected_theme = request.form["theme"]
        matched, unmatched = analyze_selection_text(contest_id, raw_text, selected_theme)
        report_text = create_selection_report_text(matched)

    return render_template(
        "selection.html",
        contest=contest,
        matched=matched,
        unmatched=unmatched,
        raw_text=raw_text,
        report_text=report_text,
        selected_theme=selected_theme,
    )

@app.route("/contest/<int:contest_id>/status", methods=["POST"])
def change_status(contest_id):

    status = request.form["status"]

    update_contest_status(contest_id, status)

    return redirect(
        url_for("contest", contest_id=contest_id)
    )

@app.route("/contest/<int:contest_id>/deadline", methods=["POST"])
def change_deadline(contest_id):

    deadline_at = request.form["deadline_at"]

    update_deadline(contest_id, deadline_at)

    return redirect(
        url_for("contest", contest_id=contest_id)
    )

@app.route("/contest/<int:contest_id>/delete", methods=["POST"])
def delete(contest_id):

    delete_contest(contest_id)

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)