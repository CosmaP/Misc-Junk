#!/usr/bin/env python

###########################################################################################
#
# Note:     This Creates Snipe IT groups
#           The Input file is manually created and must be in this format
#
#           name,default_checkout_length,max_checkout_length
#           Support,14,28
#           Consultancy,14,28
#           3E,14,28
#           Aderant,14,28
#           Intapp,14,28
#
#
###########################################################################################

import config
import requests
import csv
from datetime import datetime
import logging

# Set the API endpoint and token
api_url = config.API_URL
api_token = config.API_TOKEN
input_file = config.INPUT_FILE

###################### Set up Logging
logfile = config.LOGFILE

# get Date and time
dt_object = datetime.now()
# Create time format for Logging
modified = dt_object.strftime('_%Y-%m-%d_%H_%M')
logfile = logfile + modified + ".log"

# configure logging
FORMAT = '%(asctime)-20s %(levelname)-8s %(message)s'
logging.basicConfig(filename=logfile, level=logging.DEBUG, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')

###################### End of Logging Setup

def setupheader(api_token):
    # Set the headers
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
        }
    return headers

def createdata(input_file):
    # Define the user group data
    logging.info(f'Reading {input_file}')
    print("\n\n................... Reading " + input_file + " ................")
    # Specify file
    with open(input_file, 'r') as datafile:
        # Read file in as an ordered dictionary
        groupreader = csv.DictReader(datafile)
        data = list(groupreader)
        
    # Convert 2 fields to integers    
    for row in data:
        row['default_checkout_length'] = int(row['default_checkout_length'])
        row['max_checkout_length'] = int(row['max_checkout_length'])
   
    datafile.close()
    return data

def creategroups(api_url, headers, data):
    # Make the API request to add the user group
    logging.info('Creating groups')
    print("\n\n................... Creating groups ................\n\n")
    count = 0
    for group in data:
        response = requests.post(f'{api_url}/groups', headers=headers, json=group)
        count = count + 1
        logging.info(f'Creating group {count}: {group}')
        print(count, group)
        
    # Check the response status code
    # if response.status_code == 200 it has been successful:
    if response.status_code == 200:
        logging.info(f'{count} User groups created successfully!')
        print('\n\n' + str(count) + ' User groups created successfully!')
    else:
        logging.error(f'Error adding user groups: {response.content}')
        print('\n\nError adding user groups:', response.content)
    return response.status_code
    
    
def main():
        
    try:
        headers = setupheader(api_token)
        data = createdata(input_file)
        success = creategroups(api_url, headers, data)
        logging.info('End of Run')
        print("\n\n................... End of Run ................\n\n")
    except:
        logging.error('Create groups failed')
        print("\n\n................... Create groups failed! ................\n\n")
        exit(1)
    
   
    
    
#======================================================================	
# __main__ Code
#======================================================================	   
    
if __name__ == "__main__":
    try:
        main()
    except:
        logging.error('Create groups failed!')
        print("\n\n................... Create groups failed! ................\n\n")
    
        # end main
else:
    logging.info('Importing SnipeIT.py')
    print("\n\n................... Importing SnipeIT.py ................\n\n")
    
# End of __main__ Code
#======================================================================
