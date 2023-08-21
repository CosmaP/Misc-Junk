#!/usr/bin/env python

###########################################################################################
#
# Note:     Attempt to use Microsoft Graph
#           
# Needs
# pip install microsoftgraph-python
#
###########################################################################################

#==========================================================================================	
# Imports
#==========================================================================================

import config
import siteinfo
from microsoftgraph.client import Client

#==========================================================================================
# Some Parameters
#==========================================================================================

siteid = config.TENANTNAME
listid = siteinfo.SHAREPOINT_SITE_NAME
redirect_uri = siteinfo.REDIRECT_URI_01

#==========================================================================================	
# Set up logging.
#==========================================================================================	
 
from datetime import datetime
import logging

logfile = config.LOGFILE + "02"

# get Date and time
dt_object = datetime.now()
# Create time format for Logging
modified = dt_object.strftime('_%Y-%m-%d_%H_%M')
logfile = logfile + modified + ".log"

# configure logging
FORMAT = '%(asctime)-20s %(levelname)-8s %(message)s'
logging.basicConfig(filename=logfile, level=logging.DEBUG, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')

#==========================================================================================	
#==========================================================================================	
# Main Loop
#==========================================================================================	

def main():
    # Configure the Microsoft Graph client
    client = Client(
        client_id=config.CLIENT_ID,
        client_secret=config.CLIENT_SECRET
        )
    
    url = client.authorization_url(redirect_uri, scope="https://graph.microsoft.com/.default", state=None)

    # Retrieve user objects from SharePoint
    #users = client.get('https://graph.microsoft.com/v1.0/sites/{siteid}/lists/{listid}/items?$expand=fields').json()['value']
    
    query = ".xlsx, .xlsm"
    response = client.files.search_items(query)
    
    print(response)

    # Extract real names from user objects
    for user in users:
        user_fields = user['fields']
        user_id = user_fields['UserID']  # Replace 'UserID' with the appropriate field name for user identification
        user_real_name = user_fields['RealName']  # Replace 'RealName' with the appropriate field name for the real name
        print(f"User ID: {user_id}, Real Name: {user_real_name}")

   

#==========================================================================================	
# __main__ Code
#==========================================================================================	
    
if __name__ == "__main__":
    
    # Start
    main()
    
else:
    print("\n\n................... Importing Test02.py ................")
    
# End of __main__ Code
#==========================================================================================	