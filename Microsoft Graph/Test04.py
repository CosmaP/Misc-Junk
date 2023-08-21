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
import adal
import requests

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


        tenant = "pinnacle-oa.com"
        client_id = config.CLIENT_ID
        client_secret = config.CLIENT_SECRET

        username = config.USERNAME
        password = config.PASSWORD

        authority = "https://login.microsoftonline.com/" + tenant
        RESOURCE = "https://graph.microsoft.com"

        context = adal.AuthenticationContext(authority)

        # Use this for Client Credentials
        #token = context.acquire_token_with_client_credentials(
        #    RESOURCE,
        #    client_id,
        #    client_secret
        #    )

        # Use this for Resource Owner Password Credentials (ROPC)  
        token = context.acquire_token_with_username_password(RESOURCE, username, password, client_id);

        graph_api_endpoint = 'https://graph.microsoft.com/v1.0{0}'

        # /me only works with ROPC, for Client Credentials you'll need /<UsersObjectId/
        request_url = graph_api_endpoint.format('/me')
        headers = { 
        'User-Agent' : 'python_tutorial/1.0',
        'Authorization' : 'Bearer {0}'.format(token["accessToken"]),
        'Accept' : 'application/json',
        'Content-Type' : 'application/json'
        }

        response = requests.get(url = request_url, headers = headers)
        print (response.content)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        logging.error(f"Error: {str(e)}")

#==========================================================================================
# Entry Point
#==========================================================================================

if __name__ == "__main__":
    main()
