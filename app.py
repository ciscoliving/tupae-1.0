from datetime import datetime
from hashlib import sha256

from flask import Flask, render_template, request, redirect, url_for, session
from data import (
    load_data,
    save_data,
    create_user,
    verify_user,
    add_brand,
    add_account,
    schedule_post,
    list_posts,
)

app = Flask(__name__)
app.secret_key = "change-me"


def hash_pw(pw: str) -> str:
    return sha256(pw.encode()).hexdigest()


@app.route("/")
def index():
    if "user" not in session:
        return redirect(url_for("login"))
    data = load_data()
    return render_template("dashboard.html", posts=list_posts(), brands=data.get("brands", []))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user = request.form["username"]
        pw = hash_pw(request.form["password"])
        if create_user(user, pw):
            session["user"] = user
            return redirect(url_for("index"))
        return "User exists", 400
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pw = hash_pw(request.form["password"])
        if verify_user(user, pw):
            session["user"] = user
            return redirect(url_for("index"))
        return "Invalid credentials", 403
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/brand", methods=["POST"])
def add_brand_view():
    if "user" not in session:
        return redirect(url_for("login"))
    name = request.form["name"]
    add_brand(name)
    return redirect(url_for("index"))


@app.route("/account", methods=["POST"])
def add_account_view():
    if "user" not in session:
        return redirect(url_for("login"))
    brand = request.form["brand"]
    platform = request.form["platform"]
    username = request.form["username"]
    add_account(brand, platform, username)
    return redirect(url_for("index"))


@app.route("/schedule", methods=["POST"])
def schedule_post_view():
    if "user" not in session:
        return redirect(url_for("login"))
    brand = request.form["brand"]
    platform = request.form["platform"]
    message = request.form["message"]
    time_str = request.form.get("time")
    post_time = None
    if time_str:
        post_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M").isoformat()
    schedule_post(brand, platform, message, post_time)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
