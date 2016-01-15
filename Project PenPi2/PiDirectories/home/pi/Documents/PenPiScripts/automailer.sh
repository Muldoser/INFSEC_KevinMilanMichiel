#!/bin/bash
# Auto nmap mailing service

sudo nmap --open -O 192.168.0.*/24 192.168.1.*/24 > output.txt
cd ~/Documents/PenPiScripts/
sudo python mailnmap.py

