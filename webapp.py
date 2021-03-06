from flask import Flask, render_template, request
import hackbright
import jinja2

app = Flask(__name__)

@app.route("/")
def get_github():
    return render_template("get_github.html")

@app.route("/student")
def get_student():
    hackbright.connect_to_db()
    student_github=request.args.get("github")
    row = hackbright.get_student_by_github(student_github)
    html = render_template("student_info.html", first_name=row[0], last_name=row[1], github=row[2])
    return html


if __name__ == "__main__":
    app.run(debug=True)