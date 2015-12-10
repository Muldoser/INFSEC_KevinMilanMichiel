import subprocess
import smtplib
import socket
from email.mime.text import MIMEText
import datetime
from urllib import urlopen
import re
def getPublicIp():
        data=str(urlopen('http://checkip.dyndns.com/').read())
        return re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)
to = 'penpi.infsec@gmail.com'
today = datetime.date.today()
arg='ip route list'
p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
data = p.communicate()
split_data = data[0].split()
ipaddr = split_data[split_data.index('src')+1]
public_ip = getPublicIp()
my_ip = 'Your RPi ip is %s / %s' %  (ipaddr, public_ip)
msg = MIMEText(my_ip)
msg['Subject'] = 'IP For RaspberryPi on %s' % today.strftime('%b %d %Y')
msg['From'] = 'penpi.infsec@gmail.com'
msg['To'] = to
try :
        print("Telenet testen")
        smtpserver = smtplib.SMTP('uit.telenet.be', 25)
        smtpserver.ehlo()
        smtpserver.sendmail('penpi.infsec@gmail.com', [to], msg.as_string())
        smtpserver.quit()
        print("telenet gelukt")
except:
        print("telenet mislukt")
        pass
        print("telenet mislukt")
try :
        print("ap starten");
        msg['From'] = 'penpi.infsec@gmail.com'
        msg['To'] = 'penpi.infsec@gmail.com'
        smtpserver = smtplib.SMTP('mailrelay.ap.be', 25)
        smtpserver.ehlo()
        smtpserver.sendmail('penpi.infsec@gmail.com', ['penpi.infsec@gmail.com'], msg.as_string())
        smtpserver.quit()
        print("ap gelukt")
except:
        print("ap mislukt")
        pass
