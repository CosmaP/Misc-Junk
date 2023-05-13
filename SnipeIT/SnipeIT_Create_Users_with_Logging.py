#!/usr/bin/env python

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
        userreader = csv.DictReader(datafile)
        data = list(userreader)
 
    # Add cols for first and last names
    data.extend('first_name')
    data.extend('last_name')
    data.extend('password')
    data.extend('password_confirmation')
        
    count = 0    
    countt = len(data)
    print(countt)
    logging.debug('Data Count: ' + str(countt))
    # split Name in to first name and last name
    for row in data:
        # Split full name in 2 at the space
        names = row['Name'].split(maxsplit=1)
        # Add to list        
        row['first_name'] = names[0]
        row['last_name'] = names[1]
        
        #row['default_checkout_length'] = int(row['default_checkout_length'])
        #row['max_checkout_length'] = int(row['max_checkout_length'])
        count = count + 1
        logging.info('User Data Fixed: ' + str(count) + ' - ' + str(row))
        print(str(count) + ' - ' + str(row))
#        createusers(row)
   
    datafile.close()
    return data

def createusers(api_url, headers, data):
#def createusers(data):    
#    global api_url
#    global headers
    # Make the API request to add the user group
    logging.info('Creating users')
    print("\n\n................... Creating users ................\n\n")
    count = 0
    for user in data:
        response = requests.post(f'{api_url}/users', headers=headers, json=user)
        count = count + 1
        logging.info(f'Creating user {count}: {user}')
        print(count, user)
        
    # Check the response status code
    # if response.status_code == 200 it has been successful:
    if response.status_code == 200:
        logging.info(f'{count} User users created successfully!')
        print('\n\n' + str(count) + ' User users created successfully!')
    else:
        logging.error(f'Error adding user users: {response.content}')
        print('\n\nError adding user users:', response.content)
    return response.status_code
    
    
def main():
    global headers    
    #try:
    headers = setupheader(api_token)
    data = createdata(input_file)
    success = createusers(api_url, headers, data)
    logging.info('End of Run')
    print("\n\n................... End of Run ................\n\n")
#except:
    #    logging.error('Create users failed')
    #    print("\n\n................... Create users failed! ................\n\n")
    #    exit(1)
    
   
    
    
#======================================================================	
# __main__ Code
#======================================================================	   
    
if __name__ == "__main__":
    #try:
    main()
    #except:
    #    logging.error('Create users failed!')
    #    print("\n\n................... Create users failed! ................\n\n")
    
        # end main
else:
    logging.info('Importing SnipeIT.py')
    print("\n\n................... Importing SnipeIT.py ................\n\n")
    
# End of __main__ Code
#======================================================================
