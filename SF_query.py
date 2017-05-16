from simple_salesforce import Salesforce
import getpass
import csv
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
#   Section 1: Bait Types
# ====================================================

query_text = 'SELECT Name,name_afr__c,name_eng__c FROM Ablb_Bait_Types__c'
result, num_records, records = run_soql_query(sfc, query_text)
# write_csv('mycsv.csv',records)

# Declare a csv file:
# csv_writer = csv.writer('tempfile.csv', delimiter=',')
# wr = csv.writer(test.csv, delimiter=',')

with open('datafiles/csv/List_BaitTypes.csv', 'wb') as csvfile:
    wr = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
    if (result is not None) & (num_records > 0):
        print '\nWRITING List_BaitTypes.csv ...'
        if num_records > 0:
            wr.writerow([
                "name_key",
                "name_Eng",
                "name_Afr"
            ])
            for record in records:
                wr.writerow([
                    record['Name'],
                    record['name_eng__c'],
                    record['name_afr__c']])
                # print record['Name'] + ': ' + record['display_name__c'] + ', ' + \
                #     record['province_abbreviation__c']
        print 'Writing Complete!\r\n'

# ====================================================
#   Section 2: Catch Methods
# ====================================================


query_text = 'SELECT Name,name_afr__c,name_eng__c,trip_type__c FROM Ablb_Catch_Method__c'
result, num_records, records = run_soql_query(sfc, query_text)

with open('datafiles/csv/List_CatchMethods.csv', 'wb') as csvfile:
    wr = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
    if (result is not None) & (num_records > 0):
        print '\nWRITING List_CatchMethods.csv ...'
        if num_records > 0:
            wr.writerow([
                "name_key",
                "name_Eng",
                "name_Afr",
                "trip_type"
            ])
            for record in records:
                wr.writerow([
                    record['Name'],
                    record['name_eng__c'],
                    record['name_afr__c'],
                    record['trip_type__c']])
        print 'Writing Complete!\r\n'

# ====================================================
#   Section 3: Communities
# ====================================================

query_text = 'SELECT name_afr__c,name_eng__c,Name,province_abbreviation__c FROM Ablb_Community__c ORDER BY name_eng__c'
result, num_records, records = run_soql_query(sfc, query_text)

with open('datafiles/csv/List_Communities.csv', 'wb') as csvfile:
    wr = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
    if (result is not None) & (num_records > 0):
        print '\nWRITING List_Communities.csv ...'
        if num_records > 0:
            wr.writerow([
                "name_key",
                "province",
                "name_Eng",
                "name_Afr"
            ])
            for record in records:
                wr.writerow([
                    record['Name'],
                    record['province_abbreviation__c'],
                    record['name_eng__c'],
                    record['name_afr__c']])
        print 'Writing Complete!\r\n'

# ====================================================
#   Section 4: Fishers
# ====================================================

sub_query_text = 'SELECT Name FROM Ablb_Community__c'
result, num_records, records = run_soql_query(sfc, sub_query_text)

notOnList = ""
for record in records:
    notOnList += record['Name'] + ' '
# print "End of file: " + notOnList

# ADD_TO_END = "not_on_list,Other (not on list),Ander (nie op lys nie)," + notOnList

# Actually start the normal query now

if (EXCLUDE_TEMP_USERS):
    query_text = "SELECT abalobi_id__c,Name,primary_community__c,abalobi_usertype__c FROM User WHERE abalobi_usertype__c LIKE '%fisher%'  AND IsActive=TRUE  AND  (NOT abalobi_id__c LIKE '%tmp%')  ORDER BY primary_community__c, Name"
    ""

    print "Excluding temporary users!"
else:
    query_text = "SELECT abalobi_id__c, Name, primary_community__c, abalobi_usertype__c FROM User WHERE abalobi_usertype__c LIKE '%fisher%'  AND IsActive=TRUE ORDER BY primary_community__c, Name"


result, num_records, records = run_soql_query(sfc, query_text)

with open('datafiles/csv/List_Fishers.csv', 'wb') as csvfile:
    wr = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
    if (result is not None) & (num_records > 0):
        print '\nWRITING List_Fishers.csv ...'
        if num_records > 0:
            wr.writerow([
                "name_key",
                "display_name",
                "community"
            ])
            for record in records:
                # check for fishers  - exclude fisher_managers who are not fishers.  field may have multiple comma-separated roles
                roles = str.split(str(record['abalobi_usertype__c']), ',')
                if 'fisher' in roles:
                    wr.writerow([
                        record['abalobi_id__c'],
                        record['Name'],
                        record['primary_community__c']])
            # For loop ends here, write end of file
            # wr.writerow([
            #     "not_on_list",
            #     "Other (not on list)",
            #     "Ander (nie op lys nie)",
            #     notOnList
            # ])
        print 'Writing Complete!\r\n'

        # Generate Not on list, add spaces

# ====================================================
#   Section 5: LandingSites
# ====================================================


query_text = 'SELECT name_afr__c,name_eng__c,Name,lkup_community_id__c FROM Ablb_Landing_Site__c  ORDER BY Name'
result, num_records, records = run_soql_query(sfc, query_text)

query_community = 'SELECT Id,Name FROM Ablb_Community__c'
result2, num_records2, records2 = run_soql_query(sfc, query_community)


def getNameFromID(lookupID):
    if (DEBUG):
        print "Searching on lookup id: " + str(lookupID)
    for record in records2:
        # print record['Id']
        if (str(lookupID) == str(record['Id'])):
            if (DEBUG):
                print "MATCH FOUND: " + str(record['Name'])
            return record['Name']



with open('datafiles/csv/List_LandingSites.csv', 'wb') as csvfile:
    wr = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
    if (result is not None) & (num_records > 0):
        print '\nWRITING List_LandingSites.csv ...'
        if num_records > 0:
            wr.writerow([
                "name_key",
                "community",
                "name_Eng",
                "name_Afr"
            ])
            for record in records:
                wr.writerow([
                    record['Name'],
                    getNameFromID(record['lkup_community_id__c']),
                    record['name_eng__c'],
                    record['name_afr__c']])
        print 'Writing Complete!\r\n'

# ====================================================
#   Section 6: NoTrip_Reasons
# ====================================================

query_text = 'SELECT Name,name_afr__c,name_eng__c FROM Ablb_No_Trip_Reason__c'
result, num_records, records = run_soql_query(sfc, query_text)

with open('datafiles/csv/List_NoTrip_Reasons.csv', 'wb') as csvfile:
    wr = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
    if (result is not None) & (num_records > 0):
        print '\nWRITING List_NoTrip_Reasons.csv ...'
        if num_records > 0:
            wr.writerow([
                "name_key",
                "name_Eng",
                "name_Afr"
            ])
            for record in records:
                wr.writerow([
                    record['Name'],
                    record['name_eng__c'],
                    record['name_afr__c']])
        print 'Writing Complete!\r\n'

# ====================================================
#   Section 7: Species
# ====================================================

query_text = 'SELECT image_file__c,Name,name_afr__c,name_eng__c,priority__c FROM Ablb_Species__c ORDER BY priority__c,name_eng__c'
result, num_records, records = run_soql_query(sfc, query_text)

with open('datafiles/csv/List_Species.csv', 'wb') as csvfile:
    wr = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
    if (result is not None) & (num_records > 0):
        print '\nWRITING List_Species.csv ...'
        if num_records > 0:
            wr.writerow([
                "name_key",
                "name_Eng",
                "name_Afr",
                "image",
                "sortby"
            ])
            for record in records:
                wr.writerow([
                    record['Name'],
                    record['name_eng__c'],
                    record['name_afr__c'],
                    record['image_file__c'],
                    str(record['priority__c']).replace('.0','')])
        print 'Writing Complete!\r\n'
