#!/usr/bin/env python

#======================================================================
#
# https://github.com/sigmf/sigmf-python/tree/main
#
# Load a SigMF archive; read all samples & metadata
#
#======================================================================
# Set-up 

# config.py holds credentials that should not be shared and other setup values
import config
from datetime import datetime
import logging
import sigmf

input_file = config.INPUT_FILE
output_file = config.OUTPUT_FILE

###################### Set up Logging
logfile = config.LOGFILE

# get Date and time
dt_object = datetime.now()
# Create time format for Logging
modified = dt_object.strftime('_%Y-%m-%d_%H_%M')
logfile = logfile + modified + ".txt"

# configure logging
FORMAT = '%(asctime)-20s %(levelname)-8s %(message)s'
logging.basicConfig(filename=logfile, level=logging.INFO, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')

###################### End of Logging Setup


def setup():                 # Shutdown GPIO and Cleanup modules

    print ('\n\nSetting Up ...')

    
    
# End of set-up Procedures  
#======================================================================

#======================================================================
# Clean-up 
    
def destroy():                 # Shutdown GPIO and Cleanup modules

    print ('\n\nCleaning Up ...')

    #GPIO.cleanup()             # Release GPIO resource
    
# End of Clean-up Procedures  
#======================================================================

#======================================================================    
# Main Control Procedure
    
def maincontrol():                  # Main Control Loop

    print ('\n\nMain Loop ...')
    
    handle = sigmf.sigmffile.fromfile(input_file)
    handle.read_samples() # returns all timeseries data
    handle.get_global_info() # returns 'global' dictionary
    handle.get_captures() # returns list of 'captures' dictionaries
    handle.get_annotations() # returns list of all annotations

# End of Main Control Procedure        
#======================================================================            

#======================================================================            
# __Main__ Startup Loop        
       
if __name__ == '__main__': # If this is loaded as he main Program will start from here
        
    # Get and parse Arguments
    
    print ('\nGo ...')

    setup()           # Setup
    
    try:
        maincontrol()    # Call main loop
        destroy()     # Shutdown
        print ('\n\n................... Exit .......................')
        exit(0) # Exit Cleanly
    except KeyboardInterrupt:
        destroy()
        print ('\n\n................... Exit .......................')
        exit(1) # Exit Cleanly
        
# End of __Main__ Startup Loop 
#======================================================================



