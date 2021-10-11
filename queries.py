import io
from cs50 import SQL


from cs50 import SQL

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///data/congress.db")

data_loaded = None


beyer = db.execute("SELECT * FROM reports A JOIN legislators B ON A.first = B.first WHERE A.last  = 'Beyer'")

#print(beyer[0])

committee = db.execute("SELECT * FROM committees WHERE committee LIKE '%Intelligence'")

for row in range(len(committee)):
     print(committee[row]['committee'])

#print(committee)

reports = db.execute("SELECT * FROM reports A JOIN legislators B ON (A.first = B.first and A.last = B.last) WHERE official_full = 'John A. Yarmuth' ")

# print(reports)

for x in range(len(reports)):
    print(reports[x]['last'])
