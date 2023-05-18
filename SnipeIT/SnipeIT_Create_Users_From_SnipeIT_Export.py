#!/usr/bin/env python

###########################################################################################
#
# Note:     Users must have a first name and last name.  Add them if they do not exist
#           Password in this are place holders.  Need to work out how to set this for 
#           LDAP enabled systems
#
#           The Input file is comes from an export from Snipe-IT and must be in this format
#
# Name,Title,Email,Phone,username,Department,Location,Manager,Assets,License,Consumables,Accessories,Notes,Groups,Login Enabled
# Fred Bloggs,,,,Fred.Bloggs,,,,0,0,0,0,,,
# Bert Brown,,,,Bert.Brown,,,,1,10,0,0,,Admin 

###########################################################################################

import config
import requests
import csv
from datetime import datetime
import logging
import time

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

def createdatafromsnipeitexport(input_file):
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
        currentrowlength = len(row)
        if currentrowlength > 1:
            # Split full name in 2 at the space
            names = row['Name'].split(" ", maxsplit=1)
            # Add to list        
            row['first_name'] = names[0]
            if len(names) <= 1:
                row['Email'] = names[0] + '@pinnacle-oa.com'
            else:
                row['last_name'] = names[1]
                row['Email'] = names[0] + '.' + names[1] + '@pinnacle-oa.com'
            
            count = count + 1
            logging.info('User Data Fixed: ' + str(count) + ' - ' + str(row))
            print(str(count) + ' - ' + str(row))
    #        createusers(row)
    
    datafile.close()
    return data

def createusers(api_url, headers, data):
    # Make the API request to add the user group
    logging.info('Creating users')
    print("\n\n................... Creating users ................\n\n")
    count = 0
    wait2 = 0
    groupcount = 0
    currentrowlength = 0
    errors = 0
    for user in data:
        groupcount = groupcount + 1
        currentrowlength = len(user)
        if currentrowlength > 2 and groupcount < 101:
            
            count = count + 1
            logging.info(f'Creating user {count}: {user}')
            print(count, groupcount)
            print(user)
            response = requests.post(f'{api_url}/users', headers=headers, json=user)
            
            if response.status_code == 200:
                logging.info(f'{count} Users created successfully!')
                print('\n\n' + str(count) + ' Users created successfully!')
            else:
                errors = errors + 1
                logging.error(f'Error adding user: {errors}, {response.content}')
                print('\n\nError adding user:', errors, response.content)
        else:
            if currentrowlength > 2:
                wait1 = 0
                wait2 = wait2 + 1
                groupcount = 0
                while wait1 < 31:
                    print('Pausing for 30 seconds: ', wait1, '- Loop (this is typically 1): ', wait2)
                    time.sleep(1)
                    wait1 = wait1 + 1
            else:
                break
            
    print(errors, ' Errors')
                
    return response.status_code
    
    
def main():
    global headers    
    try:
        logging.info('Start of Run')
        print("\n\n................... start of Run ................\n\n")
        headers = setupheader(api_token)
        data = createdatafromsnipeitexport(input_file)
        success = createusers(api_url, headers, data)
        logging.info('End of Run')
        print("\n\n................... End of Run ................\n\n")
    except:
        logging.error('Create users failed')
        print("\n\n................... Create users failed! ................\n\n")
        exit(1)
    
   
    
    
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
