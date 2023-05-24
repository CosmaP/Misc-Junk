#!/usr/bin/env python

###########################################################################################
#
# Note:     This assigns licenses to existing users in Snipe
#           The Input file is comes from an export from CodeTwo and must be in this format
#           Username capitalisation must match Snipe IT usernames 
#
# number,username
# 1,Fred.Bloggs
# 2,Bert.Brown
#
###########################################################################################

import config
import requests
import csv
import json
from datetime import datetime
import logging
import time

# Set some parameters for this run
api_url = config.API_URL
api_token = config.API_TOKEN
input_file = config.INPUT_FILE
output_file = config.OUTPUT_FILE
license_id = config.LICENSE_ID
initial_seat = config.INITIAL_SEAT

###################### Set up Logging
logfile = config.LOGFILE

# get Date and time
dt_object = datetime.now()
# Create time format for Logging
modified = dt_object.strftime('_%Y-%m-%d_%H_%M')
logfile = logfile + modified + ".log"

# configure logging
FORMAT = '%(asctime)-20s %(levelname)-8s %(message)s'
logging.basicConfig(filename=logfile, level=logging.INFO, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')

###################### End of Logging Setup

def setupheader(api_token):
    # Set the headers
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
        }
    return headers

def getusernames(input_file):
    # Define the user group data
    logging.info(f'Reading {input_file}')
    print("\n\n................... Reading " + input_file + " ................")
    usersthatrequirelicenses = []    # Create and empty list
    # Specify file
    with open(input_file, 'r') as datafile:
        # Read file in as an ordered dictionary
        userreader = csv.DictReader(datafile)
        data = list(userreader)
        for row in data:
            user_data = {'username': row['username']}
            usersthatrequirelicenses.append(user_data)
      
    datafile.close()
    
    return usersthatrequirelicenses

def getuserids(api_url, headers, output_file):
    # Make the API request to get the user account info
    logging.info('Getting User Info')
    print("\n\n................... Getting ID and Username ................")
    userdetails = []
        
    response = requests.get(f'{api_url}/users?limit=200&offset=0&sort=created_at&order=desc&deleted=false&all=false"', headers=headers, verify=False)
    data = json.loads(response.content)  # Convert the response content to a dictionary
    fieldnames = ['id', 'username'] 
                
    with open(output_file, 'w', newline='') as datafile:
        # Read file in as an ordered dictionary
        userwriter = csv.DictWriter(datafile, fieldnames=fieldnames)
        userwriter.writeheader()
        
        users = data['rows']  # Access the 'rows' key in the data dictionary
        for user in users:
            if 'id' in user and 'username' in user and 'total' not in user:
                user_data = {'id': user['id'], 'username': user['username']}
                userwriter.writerow(user_data)
                userdetails.append(user_data)
        
    datafile.close()
    logging.info('ID and Username obtained and written to %s' % output_file)
    print('\n\n................... ID and Username obtained and written to %s ................' % output_file)
    return userdetails
    
def addlicenses(api_url, headers, license_id, licensesrequired, userdetails ):
    # Make the API request to add the user group
    logging.info('Adding Licenses')
    print("\n\n................... Adding Licenses ................\n\n")
    count = 0
    seat = initial_seat - 1
    runcount = 0
    wait2 = 0 
    failures = []
 
    for username1 in licensesrequired:
        index = 0
        # print(username1)
        length = len(userdetails)
        # print(length)
        for username2 in userdetails:
            index = (index + 1) % length  # Move to the next index (wrapping around if necessary)
            #print(index)
            if index == 0:
                logging.error('%s is not a user in Snipe IT.' % username1)
                print('%s is not a user in Snipe IT.' % username1)
                failures.append('%s is not a user in Snipe IT.' % username1)
                count = count - 1
                break
            user1 = username1['username'].lower()
            user2 = username2['username'].lower()
            if user1 == user2:
                # print(count, username1, username2)
                count += 1
                seat += 1
                
                currentid = username2['id']
                payload = {"assigned_to": currentid}
                logging.info(f'Adding License {count}: Seat {seat}:  {username2}')
                print(f'\n\n***************************')
                print(f'\n\nAdding License {count}: Seat {seat}:  {username2}\n\n')
                response = requests.put(f'{api_url}/licenses/{license_id}/seats/{seat}', headers=headers, verify=False, json=payload)
                runcount += 1
        
                # Check the response status code
                # if response.status_code == 200 it has been successful:
                if response.status_code == 200:
                    logging.info(f'License {count}: Seat {seat}:  {username2} added successfully!')
                    print(f'\nLicense {count}: Seat {seat}:  {username2} added successfully!')
                    # print(f'\n\n***************************')
                else:
                    logging.error(f'Error adding User license {seat}: {response.content}')
                    print('\n\nError adding User license {seat}:', response.content)
                   
                if runcount > 99:
                    logging.info(f'Pausing for 45 seconds:')
                    print('Pausing for 45 seconds:')
                    runcount = 0
                    wait1 = 0
                    wait2 = wait2 + 1
                    while wait1 < 46:
                        print('Pausing for 45 seconds: ', wait1, '- Loop (this is typically 1): ', wait2)
                        time.sleep(1)
                        wait1 = wait1 + 1
                
                    logging.info(f'Pause Over:')
                    print('\nPause Over:\n')
                    
                break   
 
    print(f'\n\n***************************')
    logging.error('Users that failed:' )   
    print(f'\n\nUsers that failed:\n')
    for failure in failures:       
        logging.error(failure)     
        print({failure})        
    return response.status_code
                
    
def main():
        
    try:
        headers = setupheader(api_token)
        userdetails = getuserids(api_url, headers, output_file)
        licensesrequired = getusernames(input_file)
        addlicenses(api_url, headers, license_id, licensesrequired, userdetails )
        # print(licensesrequired)
        
        logging.info('End of Run')
        print("\n\n................... End of Run ................\n\n")
    except:
        logging.error('Adding user licenses had some errors. Please investigate!')
        print("\n\n................... Adding user licenses had some errors. Please investigate ................")
        logging.info('End of Run')
        print("\n\n................... End of Run ................\n\n")

        exit(1)
    
   
    
    
#======================================================================	
# __main__ Code
#======================================================================	   
    
if __name__ == "__main__":
    try:
        main()
    except:
        logging.error('Adding user licenses had some errors. Please investigate')
        print("\n\n................... Adding user licenses had some errors. Please investigate ................\n\n")
        
        # end main
else:
    logging.info('Importing SnipeIT.py')
    print("\n\n................... Importing SnipeIT.py ................\n\n")
    
# End of __main__ Code
#======================================================================
