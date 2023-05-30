#!/usr/bin/env python

#======================================================================
#
# https://github.com/sigmf/sigmf-python/tree/main
#
# Load a SigMF dataset; read its annotation, metadata, and samples
#
#======================================================================
# Set-up 

# config.py holds credentials that should not be shared and other setup values
import config
from datetime import datetime
import logging
from sigmf import SigMFFile, sigmffile

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
    
    # Load a dataset
    filename = input_file # extension is optional
    signal = sigmffile.fromfile(filename)

    # Get some metadata and all annotations
    sample_rate = signal.get_global_field(SigMFFile.SAMPLE_RATE_KEY)
    sample_count = signal.sample_count
    signal_duration = sample_count / sample_rate
    annotations = signal.get_annotations()

    # Iterate over annotations
    for adx, annotation in enumerate(annotations):
        annotation_start_idx = annotation[SigMFFile.START_INDEX_KEY]
        annotation_length = annotation[SigMFFile.LENGTH_INDEX_KEY]
        annotation_comment = annotation.get(SigMFFile.COMMENT_KEY, "[annotation {}]".format(adx))

        # Get capture info associated with the start of annotation
        capture = signal.get_capture_info(annotation_start_idx)
        freq_center = capture.get(SigMFFile.FREQUENCY_KEY, 0)
        freq_min = freq_center - 0.5*sample_rate
        freq_max = freq_center + 0.5*sample_rate

        # Get frequency edges of annotation (default to edges of capture)
        freq_start = annotation.get(SigMFFile.FLO_KEY)
        freq_stop = annotation.get(SigMFFile.FHI_KEY)

        # Get the samples corresponding to annotation
        samples = signal.read_samples(annotation_start_idx, annotation_length)

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



