import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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
    #   Complete the implementation of index in such a way that it displays an HTML table summarizing: for the user currently logged in,
    #   which stocks the user owns,
    # the numbers of shares owned,
    # the current price of each stock,
    # the total value of each holding (i.e., shares times price).
    # Also display the user’s current cash balance along with a grand total (i.e., stocks’ total value plus cash).

#Odds are you’ll want to execute multiple SELECTs. Depending on how you implement your table(s), you might find GROUP BY HAVING SUM and/or WHERE of interest.
#Odds are you’ll want to call lookup for each stock.


    user_id = session.get("user_id")
    table = []
    table = db.execute("SELECT * FROM summary WHERE user_id = ?", session.get("user_id"))

    #insert current value of stocks into summary

    i = 0
    for row in table:

        symbol = table [i]['symbol']
        stock = lookup(symbol)
        pps = stock["price"]
        sumval = pps * table [i]['shares']

        db.execute("UPDATE summary SET current_value = ?, summary_value = ? WHERE user_id = ? AND symbol = ?", pps, sumval, user_id, symbol)
        i = i + 1

    newtable = db.execute("SELECT * FROM summary WHERE user_id = ?", session.get("user_id"))

    cashlist = db.execute("SELECT cash FROM users WHERE id = ?", session.get("user_id"))
    cash = cashlist[0]["cash"]

    return render_template("index.html", table=newtable, cash=cash)








@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide stock symbol", 403)

        if lookup(request.form.get("symbol")) == None:
            return apology("Stock not found", 403)

        if not request.form.get("shares"):
            return apology("must provide shares amount", 403)

        user_id = session.get("user_id")

        symbol = request.form.get("symbol")

        stock = lookup(symbol)

        stockname = stock["name"]

        stock_value = stock["price"]

        amount = request.form.get("shares")

        date_bought = datetime.now()

        bought_value = stock_value * int(amount)

        cashlist = db.execute("SELECT cash FROM users WHERE id = ?", session.get("user_id"))
        cash = cashlist[0]["cash"]

        new_cash = cash - bought_value

        if new_cash < 0:
            return apology("Not enough cash", 403)
        #update history table
        else:
            db.execute("INSERT INTO portfolio (user_id, stock_name, symbol, shares, date_bought, date_bought_value, date_bought_pps) VALUES (?, ?, ?, ?, ?, ?, ?)", user_id, stockname, symbol, amount, date_bought, float(bought_value), stock_value)
            check = db.execute("SELECT * FROM summary WHERE user_id = ? AND symbol = ?", user_id, symbol)

            #insert into summary table
            if check == []:
                db.execute("INSERT INTO summary (user_id, stock, symbol, shares, current_value) VALUES (?,?,?,?,?)", user_id, stockname, symbol, amount, stock_value)
            else:
                new_shares = check[0]["shares"] + int(amount)
                db.execute("UPDATE summary SET shares = ?, current_value=? WHERE symbol = ?", new_shares , stock_value, symbol)
            db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, user_id)
            return redirect("/")




    else:
        #give cash balance to the html template
        cashlist = db.execute("SELECT cash FROM users WHERE id = ?", session.get("user_id"))
        cash = cashlist[0]["cash"]

        return render_template("buy.html", cash=usd(cash))



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    table = []
    table = db.execute("SELECT * FROM portfolio WHERE user_id = ?", session.get("user_id"))

    #update info with market value in table
    i = 0
    for row in table:
        id = table[i]['portfolio_id']
        symbol = table[i]['symbol']
        stock = lookup(symbol)
        price = stock["price"]
        value = price * table[i]['shares']
        db.execute("UPDATE portfolio SET market_value = ?, total_market_value=? WHERE portfolio_id = ?", price, value, id)
        i = i + 1

    #give table and cash data
    portfolio = db.execute("SELECT * FROM portfolio WHERE user_id = ?", session.get("user_id"))
    cashlist = db.execute("SELECT cash FROM users WHERE id = ?", session.get("user_id"))
    cash = cashlist[0]["cash"]
    return render_template("history.html", portfolio=portfolio, cash=cash)


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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
    #Require that a user input a stock’s symbol, implemented as a text field whose name is symbol.
    #Submit the user’s input via POST to /quote.
    #Odds are you’ll want to create two new templates (e.g., quote.html and quoted.html).
    #When a user visits /quote via GET, render one of those templates, inside of which should be an HTML form that submits to /quote via POST.
    #In response to a POST, quote can render that second template, embedding within it one or more values from lookup.

    if request.method == "POST":
        if lookup(request.form.get("symbol")) != None:
            quote = lookup(request.form.get("symbol"))
            return render_template("quoted.html", quote=quote)
        else:
            return apology("Symbol not found")

    else:
        return render_template("quote.html")




@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)


        # Ensure password was submitted & confirmed
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 403)
        checkname = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        hash = generate_password_hash(request.form.get("password"))
        checkpw = db.execute("SELECT * FROM users WHERE hash = ?", hash)
        if checkname != [] or checkpw != []:
            return apology("Username or password already taken", 403)


        # insert into users table in database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), generate_password_hash(request.form.get("password")))



        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":

        if not request.form.get("symbol"):

            return apology("Must choose a stock to sell", 403)

        if not request.form.get("shares"):
            return apology("must provide shares amount", 403)

        #variables
        user_id = session.get("user_id")
        amount = int(request.form.get("shares"))
        symbol = request.form.get("symbol")


        #check if input is correct
        check = db.execute("SELECT * FROM summary WHERE symbol = ? AND user_id = ?", symbol, user_id)
        if check == []:
            return apology("Could not find stock in your Portfolio", 403)
        elif amount > int(check[0]["shares"]):
            return apology("Selected shares amount exceeds what you owns", 403)
        date_sold = datetime.now()
        stock = lookup(symbol)
        price = int(stock['price'])
        sold_worth = price * amount
        db.execute("INSERT INTO portfolio (date_sell, stock_name, shares, date_bought_value, date_bought_pps, user_id, symbol) VALUES (?,?,?,?,?,?,?)", date_sold, stock['name'], amount, sold_worth, stock['price'], user_id, symbol)
        #update new amount
        owned = int(check[0]["shares"])
        namount = owned - amount


        db.execute("UPDATE summary SET shares = ? WHERE user_id = ? AND symbol = ?", namount, user_id, symbol)
        return redirect("/")

    else:
        #use summary table
        table = db.execute("SELECT * FROM summary WHERE user_id = ?", session.get("user_id"))

        #insert current value of stocks into summary
        i = 0
        for row in table:

            symbol = table [i]['symbol']
            stock = lookup(symbol)
            db.execute("UPDATE summary SET current_value = ? WHERE symbol = ?", stock["price"], symbol)
            i = i + 1

        newtable = db.execute("SELECT * FROM summary WHERE user_id = ?", session.get("user_id"))

        cashlist = db.execute("SELECT cash FROM users WHERE id = ?", session.get("user_id"))
        cash = cashlist[0]["cash"]

        return render_template("sell.html", table=newtable, cash=cash)

@app.route("/cash", methods=["GET", "POST"])
def cash():
    """Add cash"""
    if request.method == "POST":
        addcash = float(request.form.get("cash"))
        cashlist = db.execute("SELECT cash FROM users WHERE id = ?", session.get("user_id"))
        cash = float(cashlist[0]["cash"])
        newbalance = cash + addcash
        db.execute("UPDATE users SET cash = ? WHERE id = ?", newbalance, session.get("user_id"))
        return redirect("/cash")

    else:
        cashlist = db.execute("SELECT cash FROM users WHERE id = ?", session.get("user_id"))
        cash = cashlist[0]["cash"]
        return render_template("cash.html", cash=cash)
