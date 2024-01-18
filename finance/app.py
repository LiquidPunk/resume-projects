import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    stocks = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0",
        user_id=session["user_id"],
    )
    cash = db.execute(
        "SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"]
    )[0]["cash"]
    total = cash

    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["name"] = quote["name"]
        stock["price"] = quote["price"]
        stock["value"] = stock["price"] * stock["total_shares"]
        total += stock["value"]

    return render_template("index.html", stocks=stocks, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")

        if not symbol:
            return apology("Please input a symbol")

        # Check if shares is a valid positive integer
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("Please input a positive integer for shares")

        shares = int(shares)
        quote = lookup(symbol)

        if quote is None:
            return apology("Stock not found")

        price = quote["price"]
        total_cost = price * shares
        cash = db.execute(
            "SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"]
        )[0]["cash"]

        if cash < total_cost:
            return apology("Insufficient funds")

        # Deduct the total cost from the user's cash balance
        db.execute(
            "UPDATE users SET cash = cash - :total_cost WHERE id = :user_id",
            total_cost=total_cost,
            user_id=session["user_id"],
        )

        # Insert a new transaction into the transactions table
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
            user_id=session["user_id"],
            symbol=symbol,
            shares=shares,
            price=price,
        )

        flash("Bought!")
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id = :user_id ORDER BY timestamp DESC",
        user_id=session["user_id"],
    )

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        quote = lookup(symbol)

        if not quote:
            return apology("Invalid symbol.", 400)

        return render_template("quoted.html", symbol=symbol, quote=quote)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    #
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure all fields are inputted
        if not username or not password or not confirmation:
            return apology("Please fill out all fields.", 400)

        # Ensure passwords match
        elif password != confirmation:
            return apology("Passwords do not match.", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure that username does not already exist
        if len(rows) != 0:
            return apology("username is taken", 400)

        db.execute(
            "INSERT INTO users (username, hash) VALUES(?, ?)",
            username,
            generate_password_hash(password),
        )

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # Retrieve the user's stocks
    stocks = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0",
        user_id=session["user_id"],
    )

    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")

        # Input validation
        if not symbol:
            return apology("Please input a symbol")
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("Please input a positive number")

        shares = int(shares)

        # Find the stock in the user's portfolio
        selected_stock = next(
            (stock for stock in stocks if stock["symbol"] == symbol), None
        )

        if selected_stock is None:
            return apology("Stock not found in your portfolio")

        if selected_stock["total_shares"] < shares:
            return apology("Insufficient number of shares")

        quote = lookup(symbol)
        if quote is None:
            return apology("Failed to fetch stock information")

        price = quote["price"]
        total_sale = shares * price

        # Update the user's cash balance
        db.execute(
            "UPDATE users SET cash = cash + :total_sale WHERE id = :user_id",
            total_sale=total_sale,
            user_id=session["user_id"],
        )

        # Record the sale in the transactions table (shares as negative)
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
            user_id=session["user_id"],
            symbol=symbol,
            shares=-shares,
            price=price,
        )

        flash("Sold!")
        return redirect("/")

    else:
        return render_template("sell.html", stocks=stocks)


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        # Retrieve the current password, new password, and password confirmation from the user
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        # Query the database to get the user's current hashed password
        user = db.execute(
            "SELECT * FROM users WHERE id = :user_id", user_id=session["user_id"]
        )

        if not user or not check_password_hash(user[0]["hash"], current_password):
            return apology("Invalid current password")

        if current_password == new_password:
            return apology("New password cannot be the same as the old password!")

        if new_password != confirm_password:
            return apology("New passwords do not match.")

        # Generate a new hash for the new password
        new_hashed_password = generate_password_hash(new_password)

        # Update the user's password in the database
        db.execute(
            "UPDATE users SET hash = :new_hashed_password WHERE id = :user_id",
            new_hashed_password=new_hashed_password,
            user_id=session["user_id"],
        )

        flash("Password changed successfully!")
        return redirect("/")

    else:
        return render_template("change_password.html")
