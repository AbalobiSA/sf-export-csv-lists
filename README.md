Salesforce CSV Writer - Abalobi
=====
-----
This is a simple python script which will fetch all the required CSV data
from salesforce tables, for use with ODK and OpenFn.

> NOTE: Files will be generated in the directory of the script.

### Getting Started
Clone the repo:

    $ git clone https://github.com/AbalobiSA/sf-export-csv-lists.git

Set up your dev environment:

    $ wget https://bootstrap.pypa.io/get-pip.py
    $ python get-pip.py
    $ python -m pip install simple_salesforce

Then, make the magic happen:

    $ python SF_query.py

Enter your SF username/password/securitytoken as prompted

### Debug Flags
- If `EXCLUDE_TEMP_USERS` is set to `True`, no temporary users will appear
in the `List_Fishers.csv` file. If there are no real users, this file will
appear empty.

### Optional: Hardcode your passwords during development
Create a new file in your local repo: secrets.py and add the following lines:
```
SALESFORCE_USER = "your_SF_username_here"
SALESFORCE_PWORD = "your_SF_password_here"
SALESFORCE_SEC_TOKEN = "your_SF_securitytoken_here"
```
Replace the strings with your own SF username/password/securitytoken
