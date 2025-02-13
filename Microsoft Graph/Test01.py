#!/usr/bin/env python

###########################################################################################
#
# Note:     Attempt to use Microsoft Graph
#
# Needs
# pip install shareplum
#           
###########################################################################################

#==========================================================================================	
# Imports
#==========================================================================================

from shareplum import Site
from shareplum import Office365
from shareplum.site import Version

import config
import siteinfo


#==========================================================================================
# Some Parameters
#==========================================================================================

# SharePoint Online credentials
username = config.USERNAME
password = config.PASSWORD
site_url = siteinfo.SHAREPOINT_SITE

#==========================================================================================	
# Set up logging.
#==========================================================================================	
 
from datetime import datetime
import logging
 
logfile = config.LOGFILE  + "01"

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
    # Connect to SharePoint site
    authcookie = Office365(site_url, username=username, password=password).GetCookies()
    site = Site(site_url, version=Version.v365, authcookie=authcookie)

    # SharePoint document library and file information
    document_library = siteinfo.SHAREPOINT_LIST_NAME
    file_name = "About Pinnacle for Proposals.docx"

    # Get document information
    file = site.ListItem(file_name, document_library).GetItem()
    created_by = file["Created_x0020_By"]
    modified_by = file["Modified_x0020_By"]

    # Get users' principal names
    created_by_principal = site.GetUserLoginFromEmail(created_by)
    modified_by_principal = site.GetUserLoginFromEmail(modified_by)

    # Print the principal names
    print("Created By:", created_by_principal)
    print("Modified By:", modified_by_principal)




#==========================================================================================	
# __main__ Code
#==========================================================================================	
    
if __name__ == "__main__":
    
    # Start
    main()
    
else:
    print("\n\n................... Importing Test01.py ................")
    
# End of __main__ Code
#==========================================================================================	