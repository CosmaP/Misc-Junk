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
from msal import ConfidentialClientApplication

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

logfile = config.LOGFILE + "03"

# get Date and time
dt_object = datetime.now()
# Create time format for Logging
modified = dt_object.strftime('_%Y-%m-%d_%H_%M')
logfile = logfile + modified + ".log"

# Configure logging
FORMAT = '%(asctime)-20s %(levelname)-8s %(message)s'
logging.basicConfig(filename=logfile, level=logging.DEBUG, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')

#==========================================================================================
# Main Function
#==========================================================================================

def main():
    try:
        # Configure the Microsoft Graph client
        client = Client(
            #tenant_id=config.TENANT_ID,
            client_id=config.CLIENT_SECRET_ID,
            client_secret=config.CLIENT_SECRET
        )

        # Authenticate and obtain an access token
        #client.authenticate_client_credentials(config.SCOPES)
        
        tenant_id=config.TENANT_ID
        client_id=config.CLIENT_SECRET_ID
        client_secret=config.CLIENT_SECRET

        scope = ["https://graph.microsoft.com/.default"]
        
        # Create the confidential client application
        app = ConfidentialClientApplication(
            client_id=client_id,
            client_credential=client_secret,
            authority=f"https://login.microsoftonline.com/{tenant_id}"
        )
        
        result = app.acquire_token_for_client(scopes=scope)

        # Retrieve the access token
        access_token = result["access_token"]
        print(access_token)

        # Search for files with specific extensions in SharePoint
        query = ".xlsx OR .xlsm"
        response = client.get(f"/sites/{siteid}/drive/root/search(q='{query}')")

        if response.status_code == 200:
            files = response.json().get("value")
            for file in files:
                file_name = file.get("name")
                file_path = file.get("webUrl")
                print(f"File Name: {file_name}, File Path: {file_path}")
        else:
            print("Error occurred while searching for files.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        logging.error(f"Error: {str(e)}")

#==========================================================================================
# Entry Point
#==========================================================================================

if __name__ == "__main__":
    main()
