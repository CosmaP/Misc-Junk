#!/usr/bin/env python

#======================================================================
# Set-up 

#ptpython
import pandas as pd
import csv
import os

def setup():                 # Shutdown GPIO and Cleanup modules

    print ('\n\nSetting Up ...\n')
    # Print the current working directory
    print("Current working directory: {0}".format(os.getcwd()))
    # Change the current working directory
    #os.chdir('Python_Pandas')
    # Print the current working directory
    #print("Current working directory: {0}".format(os.getcwd()))


        
# End of set-up Procedures  
#======================================================================

#======================================================================
# Clean-up 
    
def destroy():                 # Shutdown GPIO and Cleanup modules

    print ('\n\nCleaning Up ...\n')

        
# End of Clean-up Procedures  
#======================================================================

#======================================================================    
# Main Control Procedure
    
def maincontrol():                  # Main Control Loop

    print ('\n\nMain Loop ...\n')

    csvfile = open('Lottery_Powerball_Winning_Numbers__Beginning_2010.csv')
    
    LotteryReader = csv.reader(csvfile)

    # Read File 1 time
    for row in LotteryReader:
        print(row)
    print('*****************************************************************************************************************')
    print('*****************************************************************************************************************')

    # Return position in file back to the begging
    csvfile.seek(0)

    data = list(LotteryReader)

    print(data)

    header = data[0]
    data = data[1:]

    print(header)

    for i, row in enumerate(data):
        date, numbers, number = row
        if number == '':
            number = 1
        else:
            number = int(number)
        data[i] = [date, numbers, number]
    
    print(data)

    with open('Lottery_Powerball_Modified.csv', 'w') as csvfile2:
        LotteryWriter = csv.writer(csvfile2)  
        LotteryWriter.writerow(header)
        LotteryWriter.writerows(data)

    
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



