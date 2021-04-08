
#https://www.raspberrypi-spy.co.uk/2018/02/rc522-rfid-tag-read-raspberry-pi/


import sys
	import mcpi.minecraft as minecraft
	import mcpi.block as block
	import non_blocks
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
	connection = mysql.connector.connect(host='x', 
	                                        database='x',
	                                         user='x',
	                                         password='x')
	

	cursor = connection.cursor()
	print("Connected to database")
	

	def setInterval(func,time):
	    e = threading.Event()
	    while not e.wait(time):
	        func()
	

	testX, testY, testZ, targetY, targetX, targetZ = 0,0,0,0,0,0
	haveMadeEnviron, haveFinished, haveReturned = False, False, False
	

	def registerScan():
	    print('new scan')
	    global testX, testY, testZ, targetX, targetY, targetZ, haveMadeEnviron, haveFinished, haveReturned
	    testX = 30
	    testY = 30
	    testZ = 100
	    targetY = 2
	    targetX = 0
	    targetZ = 30
	    haveMadeEnviron = False
	    haveFinished = False
	    haveReturned = False
	

	    ## choose random position which is stone
	    block_beneath = block.COBBLESTONE.id;
	    while block_beneath != block_id_stone:
	        randomX, randomY, randomZ = random.randint(0,size),0,random.randint(0,size)
	        block_beneath = mc.getBlock(randomX, randomY, randomZ)  # block ID
	##        print(randomX, randomZ, block_beneath)
	        mc.player.setPos(randomX, randomY+1, randomZ)
	    
	    doScanMove()
	

	

	

	## initialisation variables
	

	mc = minecraft.Minecraft.create()
	

	block_id_stone = block.STONE_SLAB.id  
	block_id = block.GRASS.id
	block_id_air = block.AIR.id
	block_id_plant = block.MUSHROOM_RED.id
	

	randPlant = random.random()
	 
	if (randPlant < 0.1):
	    block_id_plant = block.CACTUS.id
	elif (randPlant < 0.3):
	    block_id_plant = block.FLOWER_CYAN.id
	elif (randPlant < 0.5):
	    block_id_plant = block.MUSHROOM_BROWN.id
	elif (randPlant < 0.7):
	    block_id_plant = block.FLOWER_YELLOW.id
	elif (randPlant < 0.8):
	    block_id_plant = block.SAPLING.id
	

	change_area = 4
	

	

	## camera setup
	mc.camera.setFollow(0)
	mc.camera.setPos(30,30,100)
	

	sleep(0.2)
	

	size = 512
	

	

	

	## player position
	x, y, z = mc.player.getPos()
	

	sleep(2)
	

	##while haveFinished == False:
	

	def doScanMove():
	    while True:
	        
	        x, y, z = mc.player.getPos()
	

	        global haveFinished, testX, testY, testZ, haveMadeEnviron, haveReturned 
	

	        if (haveFinished != True):
	            targetX = x
	            targetZ = z
	        
	        if (abs(testX-targetX) > 0.2) or (abs(testZ-targetZ) > 0.2):
	            mc.camera.setPos(testX, testY,testZ)
	            if (abs(testX-targetX) > 0.2):
	                testX += (targetX-testX)/4
	            if (abs(testZ-targetZ) > 0.2):
	                testZ += (targetZ-testZ)/4
	        elif ((haveFinished == True) and (haveReturned == True)):
	            print('all done!')
	            break
	        elif (haveMadeEnviron != True):  
	            mc.player.setPos(x,y+1,z)
	            mc.setBlocks(x-change_area,0,z-change_area,x+change_area,0,z+change_area,block_id)
	            haveMadeEnviron = True
	            sleep(0.1)
	            mc.setBlocks(x-change_area,1,z-change_area,x+change_area,1,z+change_area,block_id_plant)
	            sleep(0.1)
	            targetY = y
	        elif (abs(targetY-testY) > 0.2):
	            mc.camera.setPos(testX, testY, z)
	            testY += (targetY-testY)/5
	            
	        elif (haveFinished != True):
	            print('finished:: in')
	            mc.camera.setNormal(1)
	            haveFinished = True
	            sleep(1)
	            targetY = 30
	            testY += 1
	            mc.camera.setFollow(0)
	            
	

	        elif (haveReturned == False):
	            print('finished:: up')
	            targetX = 30
	            targetZ = 100
	            testZ += 1
	            testX += 1
	            haveReturned = True
	

	        
	            
	        sleep(0.05)
	

	

	

	
	

	while True: 
	    print("Waiting for scan at 51.059362, -0.330051")
	    id, text = reader.read()
	    print(id)
	    print(text)
	    sql_insert_query = """ INSERT INTO CheckInSchool (CheckInSchoolDate, PupilID, Latitude, Longitude) VALUES (%s, %s, %s, %s)"""
	       
	    
	    currentDateTime = datetime.datetime.now()
	    formatted_date = currentDateTime.strftime('%Y-%m-%d')
	    
	    insert_tuple = (formatted_date, id, 51.059362, -0.330051)
	    result  = cursor.execute(sql_insert_query, insert_tuple)
	    connection.commit()
	    print (formatted_date, " inserted id: ",id, " into database successfully")
	

	    registerScan()
	#setInterval(registerScan,5)
