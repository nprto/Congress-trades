# CONGRESS STOCK TRADE TRACKER
#### Video Demo:  <https://www.youtube.com/watch?v=7McbROr6phU>
#### Description:

## What I created, and why 
Congress Stock Trade Tracker is a web app aimed at improving scrutiny of financial transactions reported by members of the U.S. House of Representatives.

By law, U.S. legislators are required to report their stock trades and other financial transactions. Those reports are available at this House [website] (https://disclosures-clerk.house.gov/). On that website it is possible to search transaction reports by representatives' names, districts and states, which useful if you know what representative you are interested in. 

Congress Stock Trade Tracker goes a step further, allowing users to look at House members' stock trades from the perspective of the committees they serve upon. In 2012, Congress enacted the Stop Trading on Congressional Knowledge Act, or STOCK Act, to put an end to legislators using privileged information for their personal financial gain. House representatives serving on committees developing policy affecting specific industries are regularly exposed to privileged information.

Congress Stock Trade Tracker allows uesrs to select any of the House's 50 committtees, view the committee's members, and then view financial transaction reports filed by those members, looking for stock transactions potentially related to the committees the lawmakers serve on.

The House of Representative does not publish datasets on House committees and their members. Rather, I sourced that data from a [Github] (https://github.com/unitedstates/congress-legislators) dataset that is maintained by volunteers from GovTrack, ProPublica and others. 

## Files:

External opensource [datasets] (https://github.com/unitedstates/congress-legislators) used to create my database:

- legislators-current.yaml
- committee-membership-current.yaml 
- - 2021FD.txt (financial 
transacation reports, found n in 2021FD.ZIP on [House website] (https://disclosures-clerk.house.gov/public_disc/financial-pdfs/2021FD.ZIP))
- committees-current.yaml

congress.db

The following tables in congress.db correspond to above 
dataset files
committees

- legislators
- members
- reports
- committeees
- subcommittess (ultimately not used)

Python scripts used to wrangle and import data into db:
update_data.py runs these python scripts:
- legislators.py (takes data from legislators-current.yaml, adds it to db)
- members.py (takes data from committee-membership-current.yaml, adds it to db)
- reports.py (this scrapes the most recent transaction report from the House website and adds it to congress.db)
- committees.py (takes data from committees-current.yaml, adds it to db)
- subcommittees.py (ultimately not used)
- update_data.py (this script runs the five above scripts, emptying congress.db and refilling it with fresh data)

- styles.css

Templates:
- layout.html
- index.html (main page, inludes a dropdown menu to choose a committee)
- committee.htlm (displays info on chosen committe, list of members and links to a page showing each member's financial transaction reports)
- reports.html (displays a list of chosen members' reports with a link to each report)
- why.html (a page explaining why I created this project)

- application.py

## Future improvements:
As I developed this project, I frequently discovered aspects I could improve and new features to potenially add in the future. Here are some of them, including reasons I did not include them in this version:

1. Include financial transaction data for Senators. While House members transactions are available only as PDF copies of their reports, individual financial transactions filed by senators are available on the Senate website. Including those reports in my web app will requires a deep dive into web scraping. 

2. Scrape House members individual transactions from their PDF filings. This I tried but failed to do, using at least two Python libraries. In one case I was able to pull data from the PDF, but it was completely disorganized, with the Python library pdfminer outputting various transaction report PDFs in disorganized ways.

3. Help users connect the dots between House committtees and specific stocks. If I could get to a point where each reported stock transaction is added to a database, rather than just providing a PDF copy of the transaction report, then I could use the [Global Industry Classification Standard] (https://www.msci.com/our-solutions/indexes/gics) to categorize each stock by economic sector. Doing that would help users identify whether stocks that legislators buy and sell are related to the committtees they serve on. For example, it is not obvious by their names that Oneok Inc, Hess Corp and Halliburton are energy companies, and it would be good to know that if their stocks were traded by a member of the House Committee on Natural Resources.

4. Scrape data directly from GitHub. See above about learning to web scrape. Currently, adding fresh data on committees and committee members requires manually downloading the data from GitHub and adding the files to CS50 IDE.

## Final word (in case a human reads this)

CS50 has been a difficult, stimulating and rewarding experience for the past several months, and I am grateful to everyone who does the hard work making this course available. 

Thanks!

Noel Randewich