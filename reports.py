# importing required modules
from zipfile import ZipFile
from urllib.request import urlopen

import urllib.request
import csv

from cs50 import SQL

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///data/congress.db")

data_loaded = None

print('Started reports.py')

# Delete existing records in table:
db.execute("DELETE FROM reports")

# specifying the zip file name
zipurl = "https://disclosures-clerk.house.gov/public_disc/financial-pdfs/2021FD.ZIP"

urllib.request.urlretrieve(zipurl, "2021FD.ZIP")

with ZipFile(r'2021FD.ZIP', 'r') as zipObj:
   # Extract all the contents of zip file in current directory
   zipObj.extractall()
zipObj.close()

# create list of legislators
people = []

#open file and create list of dictionaries
with open('2021FD.txt') as file:
    reader = csv.DictReader(file, delimiter='\t')

    for row in reader:
        people.append(row)

        # print(row)
        # print('\n')

for x in range(len(people)):

    last = people[x]['Last']
    first = people[x]['First']
    first = first.split()[0] # get just first word in name
    filing_type = people[x]['FilingType']
    state_dst = people[x]['StateDst']
    year = people[x]['Year']
    filing_date = people[x]['FilingDate']
    doc_id = people[x]['DocID']
    link = ("https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/" + year + "/" + doc_id + ".pdf")



    # get only "Periodic" transactions
    if filing_type == "P":

        db.execute("INSERT INTO reports (last, first, filing_type, state_dst, year, filing_date, doc_id, link) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                last, first, filing_type, state_dst, year, filing_date, doc_id, link)

print('Completed reports.py')