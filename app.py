from flask import Flask, render_template, request
from services.contest_service import create_contest, get_all_contests

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


if __name__ == "__main__":
    app.run(debug=True)