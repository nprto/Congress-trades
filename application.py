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

