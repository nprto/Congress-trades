import yaml
import io
from cs50 import SQL

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///data/congress.db")

data_loaded = None

print('Started subcommittees.py')

## Data on legislators from here: https://github.com/unitedstates/congress-legislators

# Delete existing records in table:
db.execute("DELETE FROM subcommittees")

a_yaml_file = open("data/committees-current.yaml")

parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)

for x in range(len(parsed_yaml_file)):

    main_committee = parsed_yaml_file[x]['name']
    main_thomas_id = parsed_yaml_file[x]['thomas_id']
    print('##')
    print(f"Committee name: {main_committee}")

    subcommittees = parsed_yaml_file[x]
    subcommittees =subcommittees.get('subcommittees')
    if subcommittees:

        subcommittees = subcommittees

        for y in range(len(subcommittees)):
            committee = main_committee
            subcommittee = subcommittees[y]['name']
            sub_thomas_id = main_thomas_id + subcommittees[y]['thomas_id']
            print(f"Subcommittee name: {subcommittee}")

            db.execute("INSERT INTO subcommittees (committee, subcommittee, sub_thomas_id, main_thomas_id) VALUES(?, ?, ?, ?)",
                 main_committee, subcommittee, sub_thomas_id, main_thomas_id)

    else:
        subcommittees = ""

    db.execute("INSERT INTO subcommittees (committee, subcommittee, sub_thomas_id, main_thomas_id) VALUES(?, ?, ?, ?)",
                 main_committee, subcommittee, sub_thomas_id, main_thomas_id)

print('Completed subcommittees.py')






    # thomas_id = parsed_yaml_file[x]['thomas_id']
    # jurisdiction = parsed_yaml_file[x]

    # jurisdiction = jurisdiction.get('jurisdiction')
    # if jurisdiction:
    #      jurisdiction = jurisdiction
    # else:
    #      jurisdiction = ""

    # print(f"chamber: {chamber}, {name}, {jurisdiction}" )





    # # try:
    # #     print(f"{bioguide}, {first} {last}, {state}, {district}, {job}, {term_end}")

    # # except KeyError:

    # #     print("Something Wrong.")


