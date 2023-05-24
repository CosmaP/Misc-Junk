#!/usr/bin/env python

###########################################################################################
#
# Note:     Users must have a first name and last name.  Add them if they do not exist
#           Password in this are place holders.  Need to work out how to set this for 
#           LDAP enabled systems
#           This creates users from an export from CodeTwo.  It must be in this format
#
#           number,Email
#           1,Bert.Brown@test.com
#           2,Fred.Bloggs@test.com
#
#           The number is a sequence number and does not matter.  But it has to be there.
#
###########################################################################################

import config
import requests
import csv
from datetime import datetime
import logging
import time
import re

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

def createdatafromcodetwoexport(input_file):
    # Define the user group data
    logging.info(f'Reading {input_file}')
    print("\n\n................... Reading " + input_file + " ................")
    # Specify file
    with open(input_file, 'r') as datafile:
        # Read file in as an ordered dictionary
        userreader = csv.DictReader(datafile)
        data = list(userreader)        #[dict(d) for d in userreader]
        #print(data)
          
    # Add cols for fields required by Snipe IT
    #data.extend('number')
    data.extend('id')
    data.extend('Name')
    data.extend('Title')
    data.extend('first_name')
    data.extend('last_name')
    data.extend('email')
    data.extend('password')
    data.extend('password_confirmation')
    data.extend('Phone')
    data.extend('username')
    data.extend('department')
    data.extend('location')
    data.extend('manager')
    data.extend('assets')
    data.extend('license')
    data.extend('consumables')
    data.extend('accessories')
    data.extend('notes')
    data.extend('groups')
    data.extend('Login Enabled')
    
    #print(data)
        
    count = 0    
    countt = len(data)
    print(countt)
    logging.debug('Data Count: ' + str(countt))
    # split Name in to first name and last name
    for row in data:
        currentrowlength = len(row)
        
        match row:
            case 'number':
                currentrowlength = 0
            case 'Name':
                currentrowlength = 0
            case 'Title':
                currentrowlength = 0
            case 'first_name':
                currentrowlength = 0
            case 'last_name':
                currentrowlength = 0
            case 'password':
                currentrowlength = 0
            case 'password_confirmation':
                currentrowlength = 0
            case 'Phone':
                currentrowlength = 0
            case 'username':
                currentrowlength = 0
            case 'Department':
                currentrowlength = 0
            case 'Location':
                currentrowlength = 0
            case 'Manager':
                currentrowlength = 0
            case 'Assets':
                currentrowlength = 0
            case 'License':
                currentrowlength = 0
            case 'Consumables':
                currentrowlength = 0
            case 'Accessories':
                currentrowlength = 0
            case 'Notes':
                currentrowlength = 0
            case 'Groups':
                currentrowlength = 0
            case 'Login Enabled':
                currentrowlength = 0
        
        if currentrowlength > 1:
            
            name_match = re.match(r'([A-Za-z]+)\.([A-Za-z]+)@', row['Email'])
            name_match2 = re.match(r'([A-Za-z]+)\.([A-Za-z]+)-([A-Za-z]+)@', row['Email'])
            if name_match:
                first_name = name_match.group(1)
                last_name = name_match.group(2)
                name = f"{first_name} {last_name}"
                username = f"{first_name}.{last_name}"
            elif name_match2:
                first_name = name_match2.group(1)
                last_name = name_match2.group(2)
                name = f"{first_name} {last_name}"
                username = f"{first_name}.{last_name}"
            else:    
            # Handle case when Email format doesn't match expected pattern
                name_match = re.match(r'([A-Za-z]+)@', row['Email'])
                first_name = name_match.group(1)
                last_name = ''
                name = name_match.group(1)
            
            #if len(last_name) <= 1:
            #    row['Email'] = first_name + '@pinnacle-oa.com'
            #else:
            #    row['last_name'] = names[1]
            #    row['Email'] = names[0] + '.' + names[1] + '@pinnacle-oa.com'
            
            #row['number'] = ''
            row['id'] = 195
            row['Name'] = name
            row['first_name'] = first_name
            row['last_name'] = last_name
            row['Email'] = row['Email']
            row['Title'] = 'Fred'
            row['password'] = 'ABC12345678'
            row['password_confirmation'] = 'ABC12345678'
            row['Phone'] = ''
            row['username'] = username
            row['Department'] = '' 
            row['Location'] = ''
            row['Manager'] = ''
            row['Assets'] = ''
            row['License'] = ''
            row['Consumables'] = ''
            row['Accessories'] = ''
            row['Notes'] = ''
            row['Groups'] = ''
            row['Login Enabled'] = ''
            
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
            response = requests.put(f'{api_url}/users', headers=headers, json=user)
            
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
    #try:
    logging.info('Start of Run')
    print("\n\n................... Start of Run ................")
    headers = setupheader(api_token)
    data = createdatafromcodetwoexport(input_file)
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
