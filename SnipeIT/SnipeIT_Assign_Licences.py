#!/usr/bin/env python

###########################################################################################
#
# Note:     This assigns licenses to existing users in Snipe
#           The Input file is comes from an export from Snipe-IT and must be in this format
#
# Name,Title,Email,Phone,username,Department,Location,Manager,Assets,License,Consumables,Accessories,Notes,Groups,Login Enabled
# Sam Gillespie,,,,Sam.Gillespie,,,,0,0,0,0,,,
# Kevin Smith,,,,Kevin.Smith,,,,1,10,0,0,,Admin 
#
###########################################################################################

import config
import requests
import csv
import json
from datetime import datetime
import logging

# Set some parameters for this run
api_url = config.API_URL
api_token = config.API_TOKEN
input_file = config.INPUT_FILE
output_file = config.OUTPUT_FILE
license_id = config.LICENSE_ID

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
    #print(usersthatrequirelicenses)
    return usersthatrequirelicenses

def getuserids(api_url, headers, output_file):
    # Make the API request to get the user account info
    logging.info('Getting User Info')
    print("\n\n................... Getting ID and Username ................")
    userdetails = []
        
    response = requests.get(f'{api_url}/users?limit=200&offset=0&sort=created_at&order=desc&deleted=false&all=false"', headers=headers)
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
    for username1 in licensesrequired:
        print(username1)
        for username2 in userdetails:
            user1 = username1['username']
            user2 = username2['username']
            if user1 == user2:
                print(count, username1, username2)
                count += 1
                
                currentid = username2['id']
                payload = {"assigned_to": currentid}
                response = requests.put(f'{api_url}/licenses/{license_id}/seats/{count}', headers=headers, json=payload)
                logging.info(f'Adding Licenses {count}: {user2}')
                print(count, username2)
        
    # Check the response status code
    # if response.status_code == 200 it has been successful:
    if response.status_code == 200:
        logging.info(f'{count} User licenses added successfully!')
        print('\n\n' + str(count) + ' User licenses added successfully!')
    else:
        logging.error(f'Error adding User licenses: {response.content}')
        print('\n\nError adding User licenses:', response.content)
    return response.status_code
    
    
def main():
        
    #try:
    headers = setupheader(api_token)
    userdetails = getuserids(api_url, headers, output_file)
    licensesrequired = getusernames(input_file)
    addlicenses(api_url, headers, license_id, licensesrequired, userdetails )
    
    logging.info('End of Run')
    print("\n\n................... End of Run ................\n\n")
    #except:
    #    logging.error('Create groups failed')
    #    print("\n\n................... Create groups failed! ................\n\n")
    #    exit(1)
    
   
    
    
#======================================================================	
# __main__ Code
#======================================================================	   
    
if __name__ == "__main__":
    #try:
    main()
    #except:
    logging.error('Create groups failed!')
    print("\n\n................... Create groups failed! ................\n\n")
    
        # end main
else:
    logging.info('Importing SnipeIT.py')
    print("\n\n................... Importing SnipeIT.py ................\n\n")
    
# End of __main__ Code
#======================================================================