import yaml
import io
from cs50 import SQL

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///data/congress.db")

data_loaded = None

## Data on legislators from here: https://github.com/unitedstates/congress-legislators

# Delete existing records in table:
db.execute("DELETE FROM legislators")

a_yaml_file = open("data/legislators-current.yaml")

parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
# dictionary of a list of dictionaries
#print(parsed_yaml_file[1].keys())

# print(parsed_yaml_file[1]['id']['bioguide'])

print('Starting legislators.py')

for x in range(len(parsed_yaml_file)):
    bioguide = parsed_yaml_file[x]['id']['bioguide']
    name = parsed_yaml_file[x]['name']
    first= name.get('first')
    if name.get('middle'):
        middle = name.get('middle')
    else:
        middle = ""
    last = name.get('last')
    if name.get('official_full'):
        official_full = name.get('official_full')
    else:
        official_full = first + " " + last


    # print(f"{first} {middle}  {last}   official_full:  {official_full}")

    last_term = parsed_yaml_file[x]['terms'][-1]
    term_end = last_term.get('end')
    job = last_term.get('type')
    state = last_term.get('state')
    district = last_term.get('district')
    party = last_term.get('party')

    db.execute("INSERT INTO legislators (bioguide, first, middle, last,  official_full, term_end, job, state, district, party) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                   bioguide, first, middle, last, official_full, term_end, job, state,
                                       district, party)

print('Completed legislators.py')





#     for x in range(len(parsed_yaml_file[key])):
#         first = parsed_yaml_file[key][x]['first']
#         middle = parsed_yaml_file[key][x]['middle']
#         last = parsed_yaml_file[key][x]['last']
#         official_full = parsed_yaml_file[key][x]['official_full']

#         bioguide = parsed_yaml_file[key][x]['bioguide']
#         thomas_id = key

        # db.execute("INSERT INTO members (name, bioguide, thomas_id) VALUES(?, ?, ?)",
        #                      name, bioguide,thomas_id)

    # try:
    #     print(f"{bioguide}, {first} {last}, {state}, {district}, {job}, {term_end}")

    # except KeyError:

    #     print("Something Wrong.")


