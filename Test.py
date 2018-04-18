#!/usr/bin/env python


#======================================================================
# Clean-up Procedures  
    
def destroy():                 # Shutdown GPIO and Cleanup modules

    GPIO.cleanup()             # Release GPIO resource
    
# End of Clean-up Procedures  
#======================================================================

#======================================================================    
# Main Control Procedure
    
def maincontrol():                  # Main Control Loop

# Main functionality goes here

# End of Main Control Procedure        
#======================================================================            

#======================================================================            
# __Main__ Startup Loop        
       
if __name__ == '__main__': # The Program will start from here
        
    # Get and parse Arguments
    
    print ('\n\nSetting Up ...\n')

    setup()           # Setup all Lights

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

