import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    error_message = None  # Initialize error_message to None

    if request.method == "POST":

        # TODO: Add the user's entry into the database

        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        if not name or not month or not day:
            error_message = "Please fill out all fields."  # Set error_message

        else:
            db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", name, month, day)
            return redirect("/")

    # TODO: Display the entries in the database on index.html
    birthdays = db.execute("SELECT * FROM birthdays")

    return render_template("index.html", birthdays=birthdays, error_message=error_message)


@app.route("/delete/<int:id>")
def delete(id):
    # Delete the birthday entry from the database
    db.execute("DELETE FROM birthdays WHERE id = :id", id=id)
    return redirect("/")

