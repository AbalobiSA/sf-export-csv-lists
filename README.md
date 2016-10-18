Salesforce CSV Writer - Abalobi
=====
-----
This is a simple python script which will fetch all the required CSV data
from salesforce tables, for use with ODK and OpenFunction.

> NOTE: Files will be generated in the directory of the script.

### Getting Started
Clone the repo:

    $ git clone https://github.com/AbalobiSA/sf-export-csv-lists.git

Open SF_query.py and add the following details:
- Salesforce Username
- Salesforce Password
- Salesforce Security token

Then, make the magic happen:

    $ python SF_query.py

### Debug Flags
- If `EXCLUDE_TEMP_USERS` is set to `True`, no temporary users will appear
in the `List_Fishers.csv` file. If there are no real users, this file will
appear empty.
