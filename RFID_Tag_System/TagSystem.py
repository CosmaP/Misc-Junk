
#https://www.raspberrypi-spy.co.uk/2018/02/rc522-rfid-tag-read-raspberry-pi/


import sys
import random
import RPi.GPIO as GPIO
import SimpleMFRC522
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import datetime


from time import sleep
import threading


reader = SimpleMFRC522.SimpleMFRC522()
print("Opening connection to database...")
connection = mysql.connector.connect(host='192.165.0.xxx', 
                                        database='rfidtag',
                                         user='pi',
                                         password='xxxxxxxxx')


cursor = connection.cursor()
print("Connected to database")


def setInterval(func,time):
    e = threading.Event()
    while not e.wait(time):
        func()



def registerScan():
    print('new scan')
    global testX, testY, testZ, targetX, targetY, targetZ, haveMadeEnviron, haveFinished, haveReturned

def doScanMove():
    while True:
        
        global haveFinished, testX, testY, testZ, haveMadeEnviron, haveReturned 
        
        print('all done!')
            
        sleep(0.05)

while True: 
    print("Waiting for scan")
    id, text = reader.read()
    print(id)
    print(text)
    sql_insert_query = """ INSERT INTO test (date, tagid) VALUES (%s, %s)"""
       
    
    currentDateTime = datetime.datetime.now()
    formatted_date = currentDateTime.strftime('%Y-%m-%d')
    
    insert_tuple = (formatted_date, id)
    result  = cursor.execute(sql_insert_query, insert_tuple)
    connection.commit()
    print (formatted_date, " inserted id: ",id, " into database successfully")


    registerScan()
#setInterval(registerScan,5)
