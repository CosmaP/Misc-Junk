#!/usr/bin/python

import time
import RPi.GPIO as GPIO

RedLED = 16
GreenLED = 18
BlueLED = 22

# Ignore the following error message
GPIO.setwarnings(False)
    
# Set GPIO Mode
GPIO.setmode(GPIO.BOARD)

# set GPIO pins for LED's to Output

GPIO.setup(RedLED, GPIO.OUT)
GPIO.setup(GreenLED, GPIO.OUT)
GPIO.setup(BlueLED, GPIO.OUT)

GPIO.output(BlueLED, True)
GPIO.output(GreenLED, False)
GPIO.output(RedLED, False)

time.sleep(1)

GPIO.output(BlueLED, False)
GPIO.output(GreenLED, True)
GPIO.output(RedLED, False)

time.sleep(1)

GPIO.output(BlueLED, False)
GPIO.output(GreenLED, False)
GPIO.output(RedLED, True)

time.sleep(1)

GPIO.output(BlueLED, False)
GPIO.output(GreenLED, False)
GPIO.output(RedLED, False)
