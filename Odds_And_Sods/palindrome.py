#!/usr/bin/python

#======================================================================
# Place holders.  These may or may not be required

# Python 2/3 compatibility
#from __future__ import print_function

#import sys
#sys.settrace
#from glob import glob
#import itertools as it
#import os
#from operator import itemgetter
#import struct

#from imutils.object_detection import non_max_suppression
#from imutils import paths

# End of Place holders
#======================================================================
#======================================================================
# Start of Main Imports and setup constants

# Module Imports
import argparse
import time

# Constants
DefaultStart = '196'

# End of Main Imports and setup constants
#======================================================================

#======================================================================
# Initialisation procedures

def setup():   # Setup GPIO and Initalise Imports
    print ("\n... Setting Up...\n")

# End of Initialisation procedures
#======================================================================

#======================================================================
# Service Procedures
      
def reverse_string(forward):
    reverse = forward[::-1]
    return(reverse)

def add_strings(char1,char2,carry):
  final = char1 + char2 + carry
  if final > 9:
    final = final - 10
    carry = 1
  else:
    carry = 0
  return (final, carry)

def palindrome_check(CurrentValue):  
  Reversed = (reverse_string(CurrentValue))
  index = len(CurrentValue) - 1
  Palindrome = False
  Check = 0
  Loop = True
  #print('CurrentValue a', CurrentValue)
  #print('Reversed', Reversed)

  while Loop == True:
    #print('index',index)
    #print(CurrentValue[index])
    #print(Reversed[index])
    if CurrentValue[index] == Reversed[index]:
      Check = Check + 1
    #print('Check', Check)
    index = index - 1
    if index < 0:
      Loop = False
 
  if Check == len(CurrentValue):
    Palindrome = True
  return palindrome_check

def palindrome_check2(n):
    return n == n[::-1]

  # End of Service Procedures    
#======================================================================

#======================================================================
# Clean-up Procedures  

def destroy():    # Shutdown GPIO and Cleanup modules
    print ("\n... Shutting Down\n")

# End of Clean-up Procedures  
#======================================================================

#======================================================================    
# Task Procedures  

# End of Task Procedures  
#======================================================================    

#======================================================================    
# Main Control Procedure
        
def mainloop(CurrentValue):            # Main Program Loop

  Palindrome = False
  carry = 0
  final = 0

  while Palindrome == False:
    Loop = True
    CurrentPosition = len(CurrentValue) -1
    Reversed = (reverse_string(CurrentValue))
    NewValue = ''

    while Loop == True:
    
      (final, carry) = add_strings(int(CurrentValue[CurrentPosition]),int(Reversed[CurrentPosition]),int(carry))
    
      CurrentPosition =CurrentPosition - 1
      NewValue = str(final) + NewValue
      if CurrentPosition == -1:
        if carry == 1:
          NewValue = str(carry) + NewValue
          carry = 0
        Loop = False
    CurrentValue = NewValue
    DisplayCheck = (len(CurrentValue) / 100 ) 
    DisplayCheck2 =  int(len(CurrentValue) / 100 ) 
    #print('DisplayCheck', DisplayCheck)
    #print('DisplayCheck2', DisplayCheck2)
    if DisplayCheck == DisplayCheck2:
      #print('CurrentValue', CurrentValue)
      print(len(CurrentValue))
    # print('CurrentValue', CurrentValue)
    # check to see if it's a Palimdrome
    Palindrome = palindrome_check2(CurrentValue)
    if Palindrome == True:
      print('Palindrome!!')
      print(CurrentValue)
 
# End of Main Control Procedure        
#======================================================================            

#======================================================================            
# __Main__ Startup Loop        
      
if __name__ == '__main__': # The Program will start from here

  parser = argparse.ArgumentParser(description='Description of Program')
  parser.add_argument('-s',dest='StartValue', type=str , help='Initial Seed Value')    # Initial Seed Value
  args = parser.parse_args()

  if ((str(args.StartValue)) != 'None'):
    print ('\nStart Value -', args.StartValue)
    CurrentValue = str(args.StartValue)
  else:
    CurrentValue = DefaultStart
    print ('\nStart Value -', CurrentValue)

  time.sleep(1)
  
  print("\nStarting....")
  setup()
  try:
      mainloop(CurrentValue)    # Call main loop
      destroy()          # Shutdown
  except KeyboardInterrupt:
      destroy()


# End of __Main__ Startup Loop 
#======================================================================
