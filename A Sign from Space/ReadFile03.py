#!/usr/bin/env python

#======================================================================
#
# https://github.com/sigmf/sigmf-python/tree/main
#
# Create and save a Collection of SigMF Recordings from numpy arrays
# First, create a single SigMF Recording and save it to disk
#
#======================================================================
# Set-up 

# config.py holds credentials that should not be shared and other setup values
import config
from datetime import datetime
import logging
import datetime as dt
import numpy as np
import sigmf
from sigmf import SigMFFile
from sigmf.utils import get_data_type_str

input_file = config.INPUT_FILE
output_file01 = config.OUTPUT_FILE01
output_file02 = config.OUTPUT_FILE02

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
    
    # suppose we have an complex timeseries signal
    data = np.zeros(1024, dtype=np.complex64)

    # write those samples to file in cf32_le
    data.tofile(input_file)

    # create the metadata
    meta = SigMFFile(
        data_file=input_file, # extension is optional
        global_info = {
            SigMFFile.DATATYPE_KEY: get_data_type_str(data),  # in this case, 'cf32_le'
            SigMFFile.SAMPLE_RATE_KEY: 48000,
            SigMFFile.AUTHOR_KEY: 'cosma@papouis.net',
            SigMFFile.DESCRIPTION_KEY: 'All zero complex float32 example file.',
            SigMFFile.VERSION_KEY: sigmf.__version__,
        }
    )

    # create a capture key at time index 0
    meta.add_capture(0, metadata={
        SigMFFile.FREQUENCY_KEY: 915000000,
        SigMFFile.DATETIME_KEY: dt.datetime.utcnow().isoformat()+'Z',
    })

    # add an annotation at sample 100 with length 200 & 10 KHz width
    meta.add_annotation(100, 200, metadata = {
        SigMFFile.FLO_KEY: 914995000.0,
        SigMFFile.FHI_KEY: 915005000.0,
        SigMFFile.COMMENT_KEY: 'example annotation',
    })

    # check for mistakes & write to disk
    meta.tofile(output_file01) # extension is optional

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
        print ('\n\n................... Exit 1.......................\n\n')
        exit(0) # Exit Cleanly
    except KeyboardInterrupt:
        destroy()
        print ('\n\n................... Exit 2.......................\n\n')
        exit(1) # Exit Cleanly
        
# End of __Main__ Startup Loop 
#======================================================================



