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
query_text = "SELECT parent_trip__r.trip_date__c, lkup_species__r.name_eng__c, other_price_type__c, alloc_sold_crates__c, alloc_sold_number__c, alloc_sold_weight_kg__c, num_crates__c, num_items__c, weight_kg__c, other_price_for_total_batch__c, other_price_per_crate__c, other_price_per_item__c, other_price_per_kg__c FROM Ablb_Fisher_Catch__c WHERE parent_trip__r.trip_date__c > 2016-10-31 ORDER BY parent_trip__r.trip_date__c DESC"
result, num_records, records = run_soql_query(sfc, query_text)

# SELECT 
# parent_trip__r.trip_date__c
# lkup_species__r.name_eng__c
# other_price_type__c
# alloc_sold_crates__c
# alloc_sold_number__c
# alloc_sold_weight_kg__c
# num_crates__c
# num_items__c
# weight_kg__c
# other_price_for_total_batch__c
# other_price_per_crate__c
# other_price_per_item__c
# other_price_per_kg__c 
# FROM 
# Ablb_Fisher_Catch__c 
# WHERE 
# parent_trip__r.trip_date__c > LAST_YEAR 
# ORDER BY 
# parent_trip__r.trip_date__c DESC

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
            # print output_dict

            # Price types:
            # per_kg
            # total_batch
            # none
            # per_item
            # per_crate
            
            # if countNumber < 10:

            if (record['other_price_type__c'] is not None):
                # Handle single items
                if (str(record['other_price_type__c']) == 'per_item'):
                    # Calculate highest single item price
                    if (record['other_price_per_item__c']) > highestPrice:
                        highestPrice = record['other_price_per_item__c']
                    # Add result to income
                    totalIncome = totalIncome + (record['other_price_per_item__c'] * record['alloc_sold_number__c'])
                # Handle total batch
                if (str(record['other_price_type__c']) == 'total_batch'):
                    # Add result to income
                    totalIncome = totalIncome + (record['other_price_for_total_batch__c'])
                
                # Handle per crate
                if (str(record['other_price_type__c']) == 'per_crate'):
                    # Add result to income
                    totalIncome = totalIncome + (record['other_price_per_crate__c'] * record['alloc_sold_crates__c'])
                
                # Handle weight
                if (str(record['other_price_type__c']) == 'per_kg'):
                    # Add result to income
                    totalIncome = totalIncome + (record['other_price_per_kg__c'] * record['alloc_sold_weight_kg__c'])              
                
                

                    # print "Price Type: " + str(record['other_price_type__c'])
                # if (str(record['other_price_type__c']) == 'per_item'):
                    # print "Price Type: " + str(record['other_price_type__c'])
                    # print ""

        print "Total Profit: " + str(totalIncome) + "\n"
        print "Highest Single Item Price: " + str(highestPrice)


                # print output_dict
                # print record['alloc_sold_crates__c']
                # print "\n"

    print 'Writing Complete!\r\n'
