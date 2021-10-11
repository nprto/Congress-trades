import yaml
import io
from cs50 import SQL

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///data/congress.db")

data_loaded = None

## Data on legislators from here: https://github.com/unitedstates/congress-legislators

# Delete existing records in table:
db.execute("DELETE FROM members")

a_yaml_file = open("data/committee-membership-current.yaml")

parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
# dictionary of a list of dictionaries
print(parsed_yaml_file.keys())
#print(parsed_yaml_file[1].keys())

# print(parsed_yaml_file[1]['id']['bioguide'])

# print(parsed_yaml_file[1]['name']['official_full'])

print('Started members.py')

for key in parsed_yaml_file.keys():
    # print('\n')
    # print(key)

    for x in range(len(parsed_yaml_file[key])):
        name = parsed_yaml_file[key][x]['name']
        bioguide = parsed_yaml_file[key][x]['bioguide']
        thomas_id = key

        db.execute("INSERT INTO members (name, bioguide, thomas_id) VALUES(?, ?, ?)",
                              name, bioguide,thomas_id)

print('Completed members.py')

    # try:
    #     print(f"{bioguide}, {first} {last}, {state}, {district}, {job}, {term_end}")

    # except KeyError:

    #     print("Something Wrong.")


