import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

import model

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")
Utable = model.User()
Stable = model.Stock()
Htable = model.History()

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Get some values
    user_id = session["user_id"]
    porto = Stable.get_portfolio(user_id)

    total = 0
    total_stocks = 0

    # Makes json for portfolio
    for stock in porto:
        sym = stock['stock']
        # Makes sure it's up to date
        info = lookup(sym)
        cash = Stable.get_amount(user_id, sym) * info["price"]
        stock["cash"] = usd(cash)
        stock["company"] = info["name"]
        stock["price"] = info["price"]
        # Counts some values to add to total
        total += cash
        total_stocks += stock["amount"]

    # Current bank
    p_cash = Utable.get_cash(user_id)
    return render_template("homepage.html",
                           porto = porto,
                           cash = usd(p_cash),
                           total_cash = usd(total + p_cash),
                           total_stocks = total_stocks)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get some values
        user_id = session["user_id"]
        stock = request.form.get("stock").upper()

        # Gets current info about stock
        info = lookup(stock)

        # Checks for correct and complete forms
        if not info or not stock:
            return apology("invailid stock", "/buy")
        try:
            new_amount = int(request.form.get("amount"))
        except:
            return apology("Please enter a number", "/buy")
        if new_amount < 1:
            return apology("Please enter a positive number", "/buy")

        # Checks if user can afford it
        cash = info["price"]
        if Utable.get_cash(user_id) < cash*new_amount:
             return apology("Not enough cash", "/buy")

        # Take money from user
        Utable.set_cash(user_id, -cash*new_amount)

        # Create stock or add amount to stock
        if Stable.stock_zero(user_id, stock):
            Stable.add_stock(user_id, stock, new_amount)
        else:
            Stable.set_stock(user_id, stock, new_amount)

        # Note transaction
        Htable.add_transaction(user_id,
                               stock,
                               new_amount,
                               -cash*new_amount)

        # Get current bank, to show to user.
        money = Utable.get_cash(user_id)
        return render_template("buy.html", money = usd(money))
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        money = Utable.get_cash(session["user_id"])
        return render_template("buy.html", money = usd(money))

@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    """Show history of transactions"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        try:
            items = int(request.form.get("item"))
        # ALL string handeling
        except:
            items = -1
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        items = 5

    # set some values
    selected = items
    user_id = session["user_id"]

    # gets the json from sql table
    hist = Htable.get_history(user_id)

    # Adds and replaces some addional values to clean things up
    data = []
    for i,item in enumerate(hist):
        total_price = item["cash"]
        value = usd(total_price)
        item["cash"] = value
        item["price"] = usd(total_price/abs(item["amount"]))
        data.append(item)

    # Let the most recent transactions of size ITEMS show first.
    data.reverse()
    data = data[:items]

    # Show all in options
    if items == -1:
        selected = 'All'
    # Returns all the data in the file
    return render_template("history.html",
                           histo = data,
                           value = selected)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get some values
        username = username=request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", "/login", 403)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", "/login" ,403)

        # Ensure username exists and password is correct
        if not Utable.check(username, password):
            return apology("invalid username and/or password", "/login", 403)

        # Remember which user has logged in
        session["user_id"] = Utable.get_id(username)
        session["name"] = username

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
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Get some values
        user_id = session["user_id"]
        stock = request.form.get("stock").upper()

        # Checks if fields are not empty
        if not stock:
            return apology("Please enter a stock", "/quote")

        # Get current values
        info = lookup(stock)

        # Checks if stock excist
        if not info:
            return apology("Please enter valid stock name", "/quote")

        # Returs amount you have and the info from the api
        amount = Stable.get_amount(user_id, stock)
        return render_template("quote.html", info=info, amount=amount)
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html", info=None)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get some values
        username = username=request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", "/register", 403)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", "/register", 403)

        if Utable.username_taken(username):
            return render_template("register.html", taken = "USERNAME TAKEN")
            return apology("Username taken", "/register")

        # hash password
        Utable.add_user(username, password)

        user_id = Utable.get_id(username)

        # Remember which user has logged in
        session["user_id"] = user_id


        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
    return

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get some values
        user_id = session["user_id"]
        stock = request.form.get("stock").upper()
        symbol = lookup(stock)

        # Checks for correctness
        if not symbol or not stock:
            return apology("invailid stock", "/sell")
        try:
            new_amount = int(request.form.get("amount"))
        except:
            return apology("Please enter a number", "/sell")
        if new_amount < 1:
            return apology("Please enter a positive number", "/sell")

        # Current value stock
        cash = symbol["price"]

        # Set boolean for deletion if stock ends up with zero
        delete = False

        # Checks if you have enough stocks
        old_amount = Stable.get_amount(user_id, stock)
        if old_amount < new_amount:
             return apology("You only have {} stocks".format(old_amount), "/sell")
        elif old_amount == new_amount:
            delete = True

        # Makes the trade of stocks and cash, also saves a transaction
        Utable.set_cash(user_id, cash*new_amount)
        Stable.set_stock(user_id, stock, -new_amount)
        Htable.add_transaction( user_id, stock, -new_amount, cash*new_amount)

        # Deletes if neccesary
        if delete:
            Stable.delete_stock(user_id, stock)

        # Returns a list of selectables
        stocks = Stable.get_stocks(user_id)
        return render_template("sell.html", stocks = stocks)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Returns a list of selectables
        stocks = Stable.get_stocks(session["user_id"])
        return render_template("sell.html", stocks = stocks)

@app.route("/bank", methods=["GET", "POST"])
@login_required
def bank():
    """Sell shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get some values
        user_id = session["user_id"]
        password = request.form.get("password")
        money = request.form.get("money")
        choice = int(request.form.get("button"))

        # Checks for correctness
        if not password or not money:
            return apology("Please enter password and/or money", "/bank")
        try:
            money = int(money)
        except:
            return apology("Please enter a valid amount of money", "/bank")
        if money < 0:
            return apology("Please enter positive number", "/bank")

        # Checks password, just for security reasons
        if not Utable.check(Utable.get_user(user_id)[0]["username"], password):
            return apology("Password is incorrect", "/bank")

        # Switches between deposit and withdrawl
        if choice == 1 and Utable.get_cash(user_id) > money:
            Utable.set_cash(user_id, -money)
            transaction = "Withdrawl"
        elif choice == -1:
            Utable.set_cash(user_id, money)
            transaction = "Deposit"
        else:
            return apology("You don't have enough money!", "/bank")

        # Note transaction
        Htable.add_transaction(user_id, transaction, choice, money)

        # Displays current cash
        cash = Utable.get_cash(user_id)
        return render_template("bank.html", cash = usd(cash))

     # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Displays current cash
        cash = Utable.get_cash(session["user_id"])
        return render_template("bank.html", cash = usd(cash))

@app.route("/check", methods=["GET"]) #################################
def check():
    username = request.form.get("username")
    if Utable.username_taken(username):
        return jsonify(False)
    else:
        return jsonify(True)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name,"/#", e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
