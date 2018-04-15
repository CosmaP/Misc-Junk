#!/usr/bin/python

# LoadData01.py

import time
from dateutil import parser
import pymysql.cursors
import re

conn = pymysql.connect(host='192.168.xx.xx', 
                       unix_socket='/tmp/mysql.sock', 
                       user='root', 
                       passwd='xxxxxxxxxx', 
                       db='tempdata',
                       cursorclass=pymysql.cursors.DictCursor)

conn.autocommit = True

# Open the file with read only permit
f = open('Cosmic/TempTrak-180411.csv', 'r')
l = open('Cosmic/TempTrak_Import_Log.txt', 'w')
# use readline() to read the first line 
#print ('1 - *****************')
line = f.readline()
#print (line)
#print ('2 - *****************')

#line = re.sub("['()\r\n]", '', line) 

# use the read line to read further.
# If the file is not empty keep reading one line
# at a time, till the file is empty

Count = 0
lasttemp = 20
lastdate = 'Wed Apr 11 07:00:08 2018'
info = ' '

while line:
    Count = Count + 1
    #print ('3 - *****************')
    line = re.sub("['()\r\n]", '', line)
    #print (line)
    #print ('4 - *****************')
    if line == ' ':
        print ('\n************************************************************\n')
        l.write('\n************************************************************\n')
        l.write('Info - ' + str(Count) + str(info) + '\n') 
        l.write('Fixed!1 - Line' + ' ' + str(Count) + str(info) + '\n')
        print ('\n************************************************************\n')
        l.write('************************************************************\n\n')
        line = lastdate + ',' + lasttemp
    
    if line == '':
        print ('\n************************************************************\n')
        l.write('\n************************************************************\n')
        l.write('Info - ' + str(Count) + str(info) + '\n') 
        l.write('Fixed!0 - Line ' + ' ' + str(Count) + str(info) + '\n')
        print ('\n************************************************************\n')
        l.write('************************************************************\n\n')
        line = lastdate + ',' + lasttemp
    
    info = line.split(',',1)
    date = info[0]
    temp = info[1]
    l.write('Info - ' + str(info) + '\n') 

    if date == ' ':
        print ('\n************************************************************\n')
        l.write('\n************************************************************\n')
        print ('Fixed!!', date, lastdate)
        l.write('Fixed!! - Date - ' + ' ' + str(Count) + str(date)+ ' - ' + str(lastdate) + '\n')
        print ('\n************************************************************\n')
        l.write('************************************************************\n\n')
        date = lastdate
    else:
        lastdate = date

    if date == '':
        print ('\n************************************************************\n')
        l.write('\n************************************************************\n')
        print ('Fixed!!!', date, lastdate)
        l.write('Fixed!!! - Date - ' + ' ' + str(Count) + str(date)+ ' - ' + str(lastdate) + '\n')
        print ('\n************************************************************\n')
        l.write('************************************************************\n\n')
        date = lastdate
    else:
        lastdate = date
           
    if temp == ' ':
        print ('\n************************************************************\n')
        l.write('\n************************************************************\n')
        print ('Fixed!!', temp, lasttemp)
        l.write('Fixed!! - Temp - ' + ' ' + str(Count) + str(temp)+ ' - ' + str(lasttemp) + '\n')
        print ('\n************************************************************\n')
        l.write('************************************************************\n\n')
        temp = lasttemp
    else:
        lasttemp = temp

    if temp == '':
        print ('\n************************************************************\n')
        l.write('\n************************************************************\n')
        print ('Fixed!!!', temp, lasttemp)
        l.write('Fixed!!! - Temp - ' + ' ' + str(Count) + str(temp)+ ' - ' + str(lasttemp) + '\n')
        print ('\n************************************************************\n')
        l.write('************************************************************\n\n')
        temp = lasttemp
    else:
        lasttemp = temp


    #print ('5 - *****************')
    #print (info)
    #print (info[0])
    #print (info[1])
    #print ('6 - *****************')
    #print(line), date, temp
    
    try:
        with conn.cursor() as cur:
            # Create a new record
            sql = "INSERT INTO `tempdata`(`date`, `temp`) VALUES ('{0}', {1})"
            #print (sql)
            #print ('7 - *****************')
            #print (temp)
            tt = float(temp)
            #print (tt)
            #print ('8 - *****************')
            d1 = time.strptime(date, '%a %b %d %H:%M:%S %Y')
            #print ('9 - *****************')
            #print (d1)
            #print ('10 - *****************')
            d2 = time.strftime('%Y-%m-%d %H:%M:%S', d1)
            print (Count, d2) #, sep=' ', end ='\n')
            #print ('11 - *****************')
            cur.execute(sql.format(d2, tt))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            conn.commit()

        #with conn.cursor() as cur:
            # Read a single record
            #sql = "SELECT count(*) FROM `tempdata`"
            #cur.execute(sql)
            #result = cur.fetchone()
            #print ('12 - *****************')
            #print(result)
            #print ('13 - *****************')
    finally:
        conn.commit()
    line = f.readline()

#with conn.cursor() as cur
#    sql = "SELECT count(*) FROM `tempdata`"
#    cur.execute(sql)
#    result = cur.fetchone()
#    print ('*****************')
#    print(result)
#    print ('*****************')


print ('\n######################################################\n\n')
l.write('\n######################################################\n\n')
cur.execute("SELECT count(*) FROM tempdata")
for response in cur:
    print(response)
    l.write('\nDone!!! - ' + ' ' + str(Count) + str(response) + '\n')
cur.close()
print ('\n######################################################\n\n')
l.write('######################################################\n\n')

conn.close()
f.close()
l.close()

exit()
