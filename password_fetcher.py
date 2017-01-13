from simple_salesforce import Salesforce
import getpass
import csv
import json
from collections import OrderedDict
try:
    import secrets
    PROMPT_FOR_SECRETS = False
except ImportError:
    PROMPT_FOR_SECRETS = True

# ====================================================
#   BOOLEAN SWITCHES & VARIABLES
# ====================================================

# Exclude temporary users from Fishers CSV? Default: True
EXCLUDE_TEMP_USERS = True
# Output debug text? Default: False
DEBUG = False

# ====================================================
#   Query Method
# ====================================================
def run_soql_query(sfs, soql_query):
    try:
        print '---------------\r\nRunning query...'
        sf_result = sfs.query_all(soql_query)
        records = sf_result['records']
        num_records = sf_result['totalSize']
        result = sf_result['done']
        print '                  done.\r\n'
        print 'Result: ' + str(result) + ', num_records: ' + str(num_records)
        return result, num_records, records

    except Exception as e:
        print ' Exception encountered: \r\n-------\r\n' + str(e) + \
            '\r\n--------\r\n'
        return None, 0, None


def connect_to_salesforce():
    if PROMPT_FOR_SECRETS:
        user = raw_input("Username:")
        passwd = getpass.getpass("Password for " + user + ":")
        sec_token = getpass.getpass("Security token:")
    else:
        user = secrets.SALESFORCE_USER
        passwd = secrets.SALESFORCE_PWORD
        sec_token = secrets.SALESFORCE_SEC_TOKEN

    print 'Connecting to SF with username: ' + user + '...'
    sfc = Salesforce(username=user, password=passwd,
                     security_token=sec_token)

    print '                    done.\r\n'
    return sfc

sfc = connect_to_salesforce()

# ====================================================
#   Print out some calculated variables
# ====================================================

# query_text = 'SELECT Name,name_afr__c,name_eng__c FROM Ablb_Bait_Types__c'
# query_text = 'SELECT id FROM Ablb_Fisher_Trip__c ORDER BY trip_date__c DESC LIMIT 10'
query_text = "SELECT name__c, surname__c, password__c  FROM Ablb_Registration__c WHERE home_community__c = 'Lamberts Bay'  ORDER BY surname__c ASC"
result, num_records, records = run_soql_query(sfc, query_text)


# Declare a csv file:
# csv_writer = csv.writer('tempfile.csv', delimiter=',')
# wr = csv.writer(test.csv, delimiter=',')
totalIncome = 0
countNumber = 0
highestPrice = 0

if (result is not None) & (num_records > 0):
    print '\nPrinting Output ...'
    if num_records > 0:
        # print "name_key",
        # print "name_Eng",
        # print "name_Afr"
        for record in records:
            output_dict = (json.dumps(record, indent=4, sort_keys=True))
            print "Name: " + str(record['name__c']) + " " + str(record['surname__c'])
            print "Password: " + str(record['password__c'])
            print ""
            # print output_dict


    print 'Writing Complete!\r\n'
