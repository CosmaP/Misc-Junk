#!/usr/bin/python

import smbus
import time
import struct
import smtplib
import RPi.GPIO as GPIO

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Constants
DS1624_ADDRESS = 0x48
DS1624_START = 0xEE
DS1624_STOP = 0x22
DS1624_READ_TEMP = 0xAA
DS1624_READ_COUNTER = 0x48
DS1624_READ_SLOPE = 0xA9
I2Cbus = smbus.SMBus(0)
MailTo = 'Recipient@domain.com'
MailFrom = 'Sender@domain.com'
GoodTemp = 21
#Winter HighTemp = 23
#Summer HighTemp = 27
HighTemp = 27
RedLED = 16
GreenLED = 18
BlueLED = 22

#Test of read/writing I2C bus

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

def sendamessage (fromaddr, toaddrs, content):

        # Google Details
        # username = 'name@gmail.com'
        # password = 'password'

        # UATS Details
	username = 'sender@domain.com'
	password = 'password'

	subject = 'Office Temp'

        #constructing a RFC 2822 message
	msg = MIMEMultipart('alternative')
	msg['From'] = fromaddr
	msg['To'] = toaddrs
	msg['Subject'] = subject

	# Create the body of the message (a plain-text and an HTML version).
	#text = 'Hi!\nHere is the Temp in your office\n' , content, '\n'
	text = content
	html = '''\
	<html>
		<head></head>
		<body>
			<p>Hi<br><br>
            	Here is the Temp in your office<br><br>''' + content + '''
			    <br><br>
                It's Far TOO HOT!!<br>
            </p>
		</body>
	</html>
	'''

	# Record the MIME types of both parts - text/plain and text/html.
	part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')
	
	# Attach parts into message container.
	# According to RFC 2046, the last part of a multipart message, in this case
	# the HTML message, is best and preferred.
	msg.attach(part1)
	msg.attach(part2)
	
	# Send the message via Google
        # server = smtplib.SMTP('smtp.gmail.com:587')
        # Send the message via UATS
	server = smtplib.SMTP('mailserver:587')
	server.starttls()
	server.login(username,password)
	server.sendmail(fromaddr, toaddrs, msg.as_string())
	server.quit()
	print "Mail Sent"
	print msg.as_string()
	return 'Mail Sent'

# Ignore the following error message
GPIO.setwarnings(False)
    
# Set GPIO Mode
GPIO.setmode(GPIO.BOARD)

# set GPIO pins for LED's to Output
GPIO.setup(RedLED, GPIO.OUT)
GPIO.setup(GreenLED, GPIO.OUT)
GPIO.setup(BlueLED, GPIO.OUT)

#Turn warnings back on
#GPIO.setwarnings(True)

# Print to console
print "***********************************************************"
print "Start Run"
print "***********************************************************"

# Open Output file
#f = open('/home/pi/Code/TempTrak.csv','a')

# Turn on Temp Sensing
write(DS1624_START)

# Wait for 5 Seconds
time.sleep(5)

# Read temp and convert to 
t4 = converttemp(readtemp())

localtime = time.asctime(time.localtime(time.time())  )
#localtime = time.strftime(gmtime(), '%d/%m/%Y %H:%M')
#Print results to console
print localtime, ' , ', t4

#Convert results to a string
dateandtime = str(localtime)
message = dateandtime, t4 
message1 = str(message) + '\n'

#Write results to file
#f.write(message1) # python will convert \n to os.linesep

if t4 > GoodTemp: 
    if t4 > HighTemp:
        GPIO.output(BlueLED, False)
        GPIO.output(GreenLED, False)
        GPIO.output(RedLED, True)
				        #Send message
        sent = sendamessage(MailFrom, MailTo, message1)
    else:    
        GPIO.output(BlueLED, False)
        GPIO.output(GreenLED, True)
        GPIO.output(RedLED, False)
else:
    GPIO.output(BlueLED, True)
    GPIO.output(GreenLED, False)
    GPIO.output(RedLED, False)

#print "***********************************************************"		
#Close file
#f.close() # you can omit in most cases as the destructor will call if

# Turn off Temp Sensing     
write(DS1624_STOP)

# Shut down GPIO
#GPIO.cleanup()

print "***********************************************************"
print "End Run"
print "***********************************************************"	
