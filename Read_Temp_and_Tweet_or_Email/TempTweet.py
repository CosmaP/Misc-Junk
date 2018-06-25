#!/usr/bin/python

import smbus
import time
import struct
import RPi.GPIO as GPIO
import os
import sys
from twython import Twython
from datetime import datetime

#Get twitter credentials
from twitterkeys import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

# Constants
DS1624_ADDRESS = 0x48
DS1624_START = 0xEE
DS1624_STOP = 0x22
DS1624_READ_TEMP = 0xAA
DS1624_READ_COUNTER = 0x48
DS1624_READ_SLOPE = 0xA9
I2Cbus = smbus.SMBus(0)
GoodTemp = 21
#Winter HighTemp = 23
#Summer HighTemp = 27
HighTemp = 27

# Set GPIO Mode
GPIO.setmode(GPIO.BOARD)

# Ignore the following error message
GPIO.setwarnings(False)
#Turn warnings back on
#GPIO.setwarnings(True)

#Read/writing I2C bus

def write(value):
    I2Cbus.write_byte_data(DS1624_ADDRESS, value, 0)
    return -1

def readtemp():
    temp = I2Cbus.read_word_data(DS1624_ADDRESS, DS1624_READ_TEMP)
    return temp

def readcounter():
	counter = I2Cbus.read_byte_data(DS1624_ADDRESS, DS1624_READ_COUNTER)
	return counter

def readslope():
	slope = I2Cbus.read_byte_data(DS1624_ADDRESS, DS1624_READ_SLOPE)
	return slope

def converttemp (bytes):
	raw_temp = (bytes & 0x00FF) 
	raw_frac = (bytes & 0xFF00) >> 8

	a = ((( raw_temp * 256 ) + raw_frac) >> 4 ) * 0.0625
	return a

def sendatweet(tweetStr):
    print "\n"
    api = Twython(consumer_key,consumer_secret,access_token,access_token_secret)
    api.update_status(status=tweetStr)
    print "\n\nTweeted: " + tweetStr


# Print to console
print "\n\n***********************************************************"
print "Start Run"
print "***********************************************************"


# Turn on Temp Sensing
write(DS1624_START)

# Wait for 5 Seconds
time.sleep(5)

# Read temp and convert to 
t4 = converttemp(readtemp())

localtime = time.asctime(time.localtime(time.time())  )

#Convert results to a string
temp = str(t4)
#Format date and time
dateandtime = datetime.now().strftime('%-I:%M%P on %d-%m-%Y')

if t4 > GoodTemp: 
    if t4 > HighTemp:
        #Send message
        message = "The temperature in my office is " + temp + "C at " + dateandtime + " #Cheerlights Red"
    else:    
        message = "The temperature in my office is " + temp + "C at " + dateandtime + " #Cheerlights Green"
else:
    message = "The temperature in my office is " + temp + "C at " + dateandtime + " #Cheerlights Blue"

sendatweet(message)

print "\n\n***********************************************************"		

# Turn off Temp Sensing     
write(DS1624_STOP)

print "End Run"
print "***********************************************************\n\n"	


