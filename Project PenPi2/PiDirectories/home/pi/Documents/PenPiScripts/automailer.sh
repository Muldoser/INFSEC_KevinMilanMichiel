#!/bin/bash
# Auto nmap mailing service

#sudo nmap --open -O 192.168.0.* 192.168.1.*/24 > output.txt
sudo nmap -T5 192.168.0.1 > output.txt
cd ~/Documents/PenPiScripts/
sudo python mailnmap.py

