from flask import Flask, render_template, request
from database import get_connection

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create", methods=["GET", "POST"])
def create():

    if request.method == "POST":

        theme1 = request.form["theme1"]
        judge1 = request.form["judge1"]

        theme2 = request.form["theme2"]
        judge2 = request.form["judge2"]

        free_judge = request.form["free_judge"]

        conn = get_connection()

        conn.execute(
            """
            INSERT INTO contests
            (title, theme1, judge1, theme2, judge2, free_judge)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                "第1回翡翠句会",
                theme1,
                judge1,
                theme2,
                judge2,
                free_judge,
            ),
        )

        conn.commit()
        conn.close()

        return "保存しました！"

    return render_template("create.html")

if __name__ == "__main__":
    app.run(debug=True)