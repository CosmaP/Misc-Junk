#!/usr/bin/env python

###########################################################################################
#
# Note:     Fill this in later
#           
###########################################################################################

#==========================================================================================	
# Imports
#==========================================================================================

import config
import requests
import pyodbc
from datetime import datetime
import logging
import time

#==========================================================================================
# Some Parameters
#==========================================================================================

server = config.SERVER
database = config.DATABASE
username = config.USERNAME
password = config.PASSWORD
trustedconnection = config.TRUSTEDCONNECTION

#==========================================================================================	
# These are for future use.
#==========================================================================================	
 
# API Detals
api_url = config.API_URL
api_token = config.API_TOKEN
# A list of URL's to create
input_file = config.INPUT_FILE
# Results file
output_file = config.OUTPUT_FILE

#==========================================================================================	
# Set up logging.
#==========================================================================================	
 
logfile = config.LOGFILE

# get Date and time
dt_object = datetime.now()
# Create time format for Logging
modified = dt_object.strftime('_%Y-%m-%d_%H_%M')
logfile = logfile + modified + ".log"

# configure logging
FORMAT = '%(asctime)-20s %(levelname)-8s %(message)s'
logging.basicConfig(filename=logfile, level=logging.DEBUG, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')

#==========================================================================================	
# Service Functions
#==========================================================================================	
 

def connecttosql():
    logging.info(f'Connecting to {server}') 
    print(f'Connecting to {server}') 
    try:                     
        connection_string = ('DRIVER={SQL Server}; SERVER=' + server + '; DATABASE=' + database + '; trustedconnection=' + trustedconnection + '; UID='+ username +';PWD=' + password)                      
        cnxn = pyodbc.connect(connection_string)
        cursor = cnxn.cursor()
    except:
        logging.error(f'Connecting to {server} Failed')
        print(f'Connecting to {server} Failed')
        exit() 
    
    return cursor  

#==========================================================================================	
#==========================================================================================	
# Main Loop
#==========================================================================================	

def main(cursor):

    cursor.execute('SELECT _payment_url FROM blt_bill;') # where _payment_url IS NOT Null;') 
    for row in cursor:
        print('row = %r' % (row,))
        #print('********************************************************')
    
    
#==========================================================================================	
# __main__ Code
#==========================================================================================	
    
if __name__ == "__main__":
    
    # Connect to SQL Server
    cursor = connecttosql()
    
    # Start Processing
    main(cursor)
    
else:
    print("\n\n................... Importing ConnectToSQL.py ................")
    
# End of __main__ Code
#==========================================================================================	