import yaml
import io
from cs50 import SQL

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///data/congress.db")

data_loaded = None

## Data on legislators from here: https://github.com/unitedstates/congress-legislators

# Delete existing records in table:
db.execute("DELETE FROM committees")

a_yaml_file = open("data/committees-current.yaml")

parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)

print('Started committees.py')

for x in range(len(parsed_yaml_file)):

    chamber = parsed_yaml_file[x]['type']
    name = parsed_yaml_file[x]['name']

    thomas_id = parsed_yaml_file[x]['thomas_id']
    jurisdiction = parsed_yaml_file[x]

    jurisdiction = jurisdiction.get('jurisdiction')
    if jurisdiction:
         jurisdiction = jurisdiction
    else:
         jurisdiction = ""

    # print(f"chamber: {chamber}, {name}, {jurisdiction}" )

    db.execute("INSERT INTO committees (chamber, committee, thomas_id, jurisdiction) VALUES(?, ?, ?, ?)",
                chamber, name, thomas_id, jurisdiction)

print('Completed committees.py')
    # try:
    #     print(f"{bioguide}, {first} {last}, {state}, {district}, {job}, {term_end}")

    # except KeyError:

    # print("Something Wrong.")


