#!/usr/bin/env python

import os

SHAREPOINT_SITE = '<sharepoint site URL>'
SHAREPOINT_SITE_NAME = '<Site name>'

SHAREPOINT_DOC = 'Shared%20Documents'
SHAREPOINT_LIST_NAME = 'Shared%20Documents'

EXPORTTYPE = 'CSV'
OUTPUTPATH = 'C:\\Data\\SharePointFiles'
OUTPUTFILE = 'SharePointFileList'
LOGPATH = 'C:\\Data'
FOLDERNAME = ''

CRAWLFOLDERS = 'Yes'

#======================================================================            
# __Main__ Startup Loop  
    
if __name__ == '__main__': # If this is loaded as he main Program will start from here
        
    print(f"\nYou can't run {os.path.basename(__file__)}!\n\n")
	
else:
    print(f"\n{os.path.basename(__file__)} imported!\n\n")

# End of __Main__ Startup Loop 
#======================================================================
