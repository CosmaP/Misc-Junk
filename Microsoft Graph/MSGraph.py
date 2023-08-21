#!/usr/bin/env python

#======================================================================
# Set-up 

# config.py holds credentials that should not be shared and other setup values
import config
from datetime import datetime
import logging

from O365 import Account

my_client_id = config.CLIENT_ID
my_client_secret = config.CLIENT_SECRET
my_tenant_id = config.TENANT_ID

###################### Set up Logging
logfile = config.LOGFILE

# get Date and time
dt_object = datetime.now()
# Create time format for Logging
modified = dt_object.strftime('_%Y-%m-%d_%H_%M')
logfile = logfile + modified + ".txt"

# configure logging
FORMAT = '%(asctime)-20s %(levelname)-8s %(message)s'
logging.basicConfig(filename=logfile, level=logging.DEBUG, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')

###################### End of Logging Setup


def setup():                 # Shutdown GPIO and Cleanup modules

    print ('\n\nSetting Up ...\n')

    
    
# End of set-up Procedures  
#======================================================================

#======================================================================
# Clean-up 
    
def destroy():                 # Shutdown GPIO and Cleanup modules

    print ('\n\nCleaning Up ...\n')

    #GPIO.cleanup()             # Release GPIO resource
    
# End of Clean-up Procedures  
#======================================================================

#======================================================================    
# Main Control Procedure
    
def maincontrol():                  # Main Control Loop

    print ('\n\nMain Loop ...\n')
    
    credentials = ('my_client_id', 'my_client_secret')
    
    # the default protocol will be Microsoft Graph
    # the default authentication method will be "on behalf of a user"

    account = Account(credentials, auth_flow_type='credentials', tenant_id=my_tenant_id)
    if account.authenticate():
        print('Authenticated!')
    else:
        print('NOT Authenticated!')
        
    print(';')

    # 'basic' adds: 'offline_access' and 'https://graph.microsoft.com/User.Read'
    # 'message_all' adds: 'https://graph.microsoft.com/Mail.ReadWrite' and 'https://graph.microsoft.com/Mail.Send'
    
    
    
    

# Main functionality goes here

# End of Main Control Procedure        
#======================================================================            

#======================================================================            
# __Main__ Startup Loop        
       
if __name__ == '__main__': # If this is loaded as he main Program will start from here
        
    # Get and parse Arguments
    
    setup()           # Setup

    print ('\nGo ...\n\n')
	
    try:
        maincontrol()    # Call main loop
        destroy()     # Shutdown
        print ('\n\n................... Exit .......................\n\n')
        exit(0) # Exit Cleanly
    except KeyboardInterrupt:
        destroy()
        print ('\n\n................... Exit .......................\n\n')
        exit(0) # Exit Cleanly
        
# End of __Main__ Startup Loop 
#======================================================================



