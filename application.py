import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# check if an int, adapted from substack

# hold_committee is going to be a global variable usable across functions
hold_committee = "x"

def isint(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
# app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///data/congress.db")


@app.route("/")
#@login_required
def index():
    """Show Committees"""

    committees =  db.execute("SELECT * FROM committees WHERE chamber IN ('house', 'joint') ORDER BY committee")

    # make a list of names for drop down menu
    names = []

    for x in range(len(committees)):
       # print(committees[x]['name'])
       names.append(committees[x]['committee'])

    return render_template("index.html", names = names)

@app.route("/why", methods=["GET"])
def why():
    return render_template("why.html")


@app.route("/committee", methods=["GET", "POST"])
def committee():

    if request.method == ("GET"):
        return render_template("/index.html")

    if request.method == ("POST"):
        #global committee #just added
        committee = request.form.get("committee")
        committee =  db.execute("SELECT * FROM committees WHERE committee = ?", committee)[0]
        global hold_committee
        hold_committee = committee['committee']

        #jurisdiction = db.execute("SELECT jurisdiction FROM committees WHERE name = ?", committee)[0]['jurisdiction']
        print(f"Chose this committee {hold_committee}")

        members = db.execute("SELECT * FROM members A JOIN committees B ON A.thomas_id = B.thomas_id JOIN legislators C ON C.bioguide = A.bioguide WHERE A.thomas_id = ?", committee['thomas_id'])

        # TODO - see if members have filed reports
        for x in range(len(members)):
            # print(members[x]['name'])
            if db.execute("SELECT * FROM reports A JOIN legislators B ON (A.first = B.first and A.last = B.last) WHERE official_full = ?" , members[x]['name']):
                members[x]['report'] = 'Yes'
                # print('YES')
            else:
                members[x]['report'] = 'No'
                # print("NO")
        members.sort(key=lambda item: item.get('report'), reverse = True)


        return render_template("committee.html", committee = committee, members = members)


@app.route("/reports", methods=["GET", "POST"])
def reports():

    if request.method == ("GET"):
        return render_template("index.html")

    if request.method == ("POST"):
        person = request.form.get('person')
        print(f" clicked on this {person}")

        print(hold_committee)
        #print(f" Belongs to this committee:{committee}")


        reports = db.execute("SELECT * FROM reports A JOIN legislators B ON (A.first = B.first and A.last = B.last) WHERE official_full = ? AND filing_type = 'P' ORDER BY filing_date DESC " , person)


        #members = db.execute("SELECT * FROM members A JOIN committees B ON A.thomas_id = B.thomas_id JOIN legislators C ON C.bioguide = A.bioguide WHERE A.thomas_id = ?", committee['thomas_id'])


        return render_template("reports.html", reports = reports,
                                            person = person,
                                            hold_committee = hold_committee)






    # account = db.execute("SELECT * FROM portfolio WHERE user_id = ?", session["user_id"])
    # username = (db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]['username']).capitalize()

    # # ? update acccount dict with price and value?
    # total = 0

    # for index in range(len(account)):
    #     account[index]['company'] = lookup(account[index]['symbol'])['name']
    #     account[index]['price'] = usd(float(lookup(account[index]['symbol'])['price']))
    #     account[index]['gain_loss'] = round((float(lookup(account[index]['symbol'])['price']) -
    #                                          float(account[index]['buy_price']))/float(account[index]['buy_price'])*100, 1)
    #     account[index]['gain_loss'] = '{:+}'.format(account[index]['gain_loss'])
    #     account[index]['buy_price'] = usd(float(account[index]['buy_price']))
    #     account[index]['total'] = usd(float(lookup(account[index]['symbol'])['price']) * account[index]['shares'])

    #     total = total + lookup(account[index]['symbol'])['price'] * account[index]['shares']

    #     # format pct chng to show "-" if negative
    #     # pct_chng = '{:+}'.format(pct_chng)

    #     print(f"pct chng: {account[index]['gain_loss'] }")

    # cash = usd(db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]['cash'])
    # total = usd(total + db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]['cash'])

#     return apology("/ page")


# @app.route("/buy", methods=["GET", "POST"])
# @login_required
# def buy():
#     """Buy shares of stock"""

#     # when requested via GET, should display form to buy a stock
#     # when form is submitted viag POST, purchase the stock fi use can afford
#     # will need to query db for amt of cash, compare to price of stock x shares
#     # if user can buy, will need to add one or more tables to finance db
#     # what tables and columns re is up to me. what stock bought was, how many shares,
#     # and who bought that stock.

#     # display results by implementing index

#     if request.method == "GET":
#         return render_template("buy.html")

#     if request.method == "POST":

#         symbol = request.form.get("symbol")

#         # check to see if valid symbol:
#         if not lookup(symbol):
#             return apology("Symbol does not exist")

#         if isint(request.form.get("shares")) == False:
#             return apology("Must be a digit that is a whole number")

#         if int(request.form.get("shares")) < 1:
#             return apology("Number must be greater than zero")

#         if int(request.form.get("shares")) % 1 != 0 or int(request.form.get("shares")) < 1:
#             return apology("Shares must be a whole number greater than 0")

#         symbol = request.form.get("symbol").upper()
#         shares = int(request.form.get("shares"))
#         price = lookup(symbol)['price']
#         cost = shares * price

#         print(symbol)
#         print(shares)
#         print(price)
#         print(cost)

#         cash = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]['cash']
#         username = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]['username']
#         print(username)

#         balance = cash - cost
#         print(balance)

#         if cost > cash:
#             return apology("You don't have enough cash")

#         if cost <= cash:
#             # add shares to portfolio
#             # add shares to porfolio for first time
#             # add shares to existing shares

#             # If the symbol is not in portfolio
#             if not db.execute("SELECT * FROM portfolio WHERE user_id = ? AND symbol = ?",
#                               session["user_id"], symbol):

#                 db.execute("INSERT INTO portfolio (username, user_id, symbol, shares, buy_price) VALUES(?, ?, ?, ?, ?)",
#                           username, session["user_id"], symbol, shares, price)

#             # If the symbol is already in portfolio, add the new shares
#             else:
#                 exist_shares = db.execute("SELECT * FROM portfolio WHERE user_id = ? AND symbol = ?",
#                                           session["user_id"], symbol)[0]['shares']
#                 exist_buyprice = db.execute("SELECT * FROM portfolio WHERE user_id = ? AND symbol = ?",
#                                             session["user_id"], symbol)[0]['buy_price']

#                 combined_shares = int(shares + exist_shares)

#                 combined_price = ((int(exist_shares) * float(exist_buyprice)) + (int(shares) * float(price))) / combined_shares

#                 print("combined_shares:")
#                 print(combined_shares)
#                 print("combined_price:")

#                 print("exist_buyprice:")
#                 print(exist_buyprice)

#                 print(symbol)

#                 db.execute("UPDATE portfolio SET shares = ?, buy_price = ? WHERE symbol = ? AND user_id = ?",
#                           combined_shares, combined_price, symbol, session["user_id"])

#             # remove cash from balance
#             db.execute("UPDATE users SET cash = ? WHERE id = ?", balance, session["user_id"])

#             # add to transactions
#             db.execute("INSERT INTO transactions (username, user_id, symbol, shares, price, cost, transact) VALUES(?,?,?,?,?,?,?)",
#                       username, session["user_id"], symbol, shares, price, cost, "Purchase")

#             return redirect("/")

#     return apology("TODO")


# @app.route("/history")
# @login_required
# def history():
#     """Show history of transactions"""

#     history = db.execute("SELECT * FROM transactions WHERE user_id = ?", session["user_id"])
#     username = (db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]['username']).capitalize()

#     for index in range(len(history)):
#         history[index]['company'] = lookup(history[index]['symbol'])['name']
#         history[index]['price'] = usd(float(lookup(history[index]['symbol'])['price']))

#     return render_template("history.html", history=history, username=username)


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     """Log user in"""

#     # Forget any user_id
#     session.clear()

#     # User reached route via POST (as by submitting a form via POST)
#     if request.method == "POST":

#         # Ensure username was submitted
#         if not request.form.get("username"):
#             return apology("must provide username", 403)

#         # Ensure password was submitted
#         elif not request.form.get("password"):
#             return apology("must provide password", 403)

#         # Query database for username
#         rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

#         # Ensure username exists and password is correct
#         if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
#             return apology("Invalid username and/or password. Try again", 403)

#         # Remember which user has logged in
#         session["user_id"] = rows[0]["id"]

#         # Redirect user to home page
#         return redirect("/")

#     # User reached route via GET (as by clicking a link or via redirect)
#     else:
#         return render_template("login.html")


# @app.route("/logout")
# def logout():
#     """Log user out"""

#     # Forget any user_id
#     session.clear()

#     # Redirect user to login form
#     return redirect("/")


# @app.route("/quote", methods=["GET", "POST"])
# @login_required
# def quote():
#     """Get stock quote."""

#     if request.method == "GET":
#         return render_template("quote.html")

#     if request.method == "POST":
#         quote = lookup(request.form.get("symbol"))

#         if not quote:
#             return apology("No such symbol")

#         else:
#             price = usd(quote['price'])
#             return render_template("quoted.html", quote=quote, price=price)

#     return apology("error")


# @app.route("/register", methods=["GET", "POST"])
# def register():
#     """Register user"""
#     # Forget any user_id
#     session.clear()
#     if request.method == "GET":
#         return render_template("register.html")

#     if request.method == "POST":

#         # add some more code for error checking,
#         # like existing names, invalid inputs. display apology if name taken

#         # Ensure username was submitted
#         if not request.form.get("username"):
#             return apology("must provide username")

#         # Ensure password was submitted
#         elif not request.form.get("password"):
#             return apology("must provide password")

#         # Ensure password was submitted second time
#         elif not request.form.get("confirmation"):
#             return apology("must repeat password")

#         elif request.form.get("password") != request.form.get("confirmation"):
#             return apology("Passwords don't match")

#         elif db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username")):
#             return apology("User already exists")

#         db.execute("INSERT INTO users(username, hash) VALUES(?, ?)",
#                   (request.form.get("username")).lower(), generate_password_hash(request.form.get("password")))

#         # Now log in
#         rows = db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username")).lower())

#         # Ensure username exists and password is correct
#         if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
#             return apology("invalid username and/or password")

#         # Remember which user has logged in
#         session["user_id"] = rows[0]["id"]

#         return redirect("/")


# @app.route("/sell", methods=["GET", "POST"])
# @login_required
# def sell():
#     """Sell shares of stock"""

#     if request.method == "GET":
#         portfolio = db.execute("SELECT * FROM portfolio WHERE user_id = ?", session["user_id"])

#         symbols = []
#         for x in range(len(portfolio)):
#             print(portfolio[x]['symbol'])
#             symbols.append(portfolio[x]['symbol'])

#         print(symbols)

#         return render_template("sell.html", symbols=symbols)

#     if request.method == "POST":

#         # check to see if valid symbol:
#         symbol = request.form.get("symbol")
#         if not lookup(symbol):
#             return apology("No such symbol")

#         # make sure shares is an integer and greater than zero
#         if isint(request.form.get("shares")) == False:
#             return apology("Must be a digit that is a whole number")

#         if int(request.form.get("shares")) < 1:
#             return apology("Number must be greater than zero")

#         symbol = request.form.get("symbol").upper()
#         shares = int(request.form.get("shares"))
#         price = lookup(symbol)['price']
#         cost = shares * price
#         username = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]['username']

#         # Check if the number is not a positive integer
#         if shares < 1:
#             return apology("Must sell at least one share")

#         # check if user has enough shares to sell
#         if shares > db.execute("SELECT * FROM portfolio WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)[0]['shares']:
#             return apology("You don't own that many shares")

#         # if own exact number of shares
#         if shares == db.execute("SELECT * FROM portfolio WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)[0]['shares']:
#             # - then delete shares from portoflio
#             db.execute("DELETE FROM portfolio WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)

#         # if selling only some shares:
#         elif shares < db.execute("SELECT * FROM portfolio WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)[0]['shares']:
#             # - then subtract shares from share count in portfolio
#             existing_shares = db.execute("SELECT * FROM portfolio WHERE user_id = ? AND symbol = ?",
#                                          session["user_id"], symbol)[0]['shares']

#             db.execute("UPDATE portfolio SET shares = ? WHERE symbol = ? AND user_id = ?",
#                       existing_shares - shares, symbol, session["user_id"])

#         # put cash form sale in user
#         cash = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]['cash']
#         balance = cash + cost
#         db.execute("UPDATE users SET cash = ? WHERE id = ?", balance, session["user_id"])

#         # add transaction history
#         db.execute("INSERT INTO transactions (username, user_id, symbol, shares, price, cost, transact) VALUES(?,?,?,?,?,?,?)",
#                   username, session["user_id"], symbol, shares, price, cost, "Sale")

#         return redirect("/")


# @app.route("/trade", methods=["GET", "POST"])
# @login_required
# def trade():
#     """Sell shares of stock via portfolio screen"""
#     if request.method == "GET":

#         return render_template("trade.html")

#     if request.method == "POST":
#         symbol = request.form.get("symbol").upper()
#         print(symbol)
#         return render_template("trade.html")
#         return apology("TODO")

#     return apology("TODO")


# def errorhandler(e):
#     """Handle error"""
#     if not isinstance(e, HTTPException):
#         e = InternalServerError()
#     return apology(e.name, e.code)


# # Listen for errors
# for code in default_exceptions:
#     app.errorhandler(code)(errorhandler)
