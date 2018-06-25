#!/bin/bash

cd /home/pi/Code/
sudo python /home/pi/Code/TempRead03.py > TempRead03.txt
sleep 5
cat TempRead03.txt


