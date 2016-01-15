Project PenPi
==============
*Kevin Van de Mieroop, Milan Willems & Michiel Mulder*

Mappen
---------

 - **[(PreProject)Documentatie](https://github.com/Muldoser/INFSEC_KevinMilanMichiel/tree/master/(PreProject)Documentatie)**

	Oefeningen op virtual machines van voor de start van het project. Niet meer gebruikt in PenPi2.

 - **[PenPi2 2014](https://github.com/Muldoser/INFSEC_KevinMilanMichiel/tree/master/PenPI%202014)**

	Oorspronkelijk project, gebruikt om op verder te gaan.

 - **[Project PenPi2](https://github.com/Muldoser/INFSEC_KevinMilanMichiel/tree/master/Project%20PenPi2)**
 
	'*Working directory*', this is where the magic happens. Hier werken we zelf dus aan het project.

Opgave
------

Je werkt voort aan één van de projecten van vorig jaar waar het onderwerp  “ raspberry pi + wifi hacking mbv wifite “ (Pentesting met Raspberry Pi=>Penpi)  was. Je maakt gebruikt van één van de bestaande projecten (van vorig jaar) en breidt deze gevoelig uit met aanvullingen.

Het wifite script laat toe om mbv van een Raspberry Pi (rpi) toestel draadloze netwerken te hacken. Doel van de opdracht is dit script verder te automatiseren zodat extra user input nihil is. Aanvullingen kunnen ook andere aanvallen zijn (bv WPA 1 kraken, password sniffing, portscanning, etc) alsook verbeterde rapportage (de huidige projecten sturen geregeld informatie over de status van het al dan niet gekraakte netwerk naar de RPI-owner)

Je gebruikt een AWUS036H Wifi usb adapter waarvan er 6-tal beschikbaar zijn (deze heeft de hoogste compatibiliteit).

(In bijlage: originele opgaven, alsook de besteoplossing van vorig jaar)

Bijlagen
--------
[Appendix originele opgave (pdf)](https://blackboard.ap.be/bbcswebdav/pid-704231-dt-content-rid-4395084_1/xid-4395084_1)

[PenPi (zip)](https://blackboard.ap.be/bbcswebdav/pid-704231-dt-content-rid-4395085_1/xid-4395085_1)

<br/>

-----
-----
-----
<br/>

Project PenPi - The Sequel
==========================

Inleiding
---------

We hebben gekozen voor het project rond de Raspberry Pi omdat 2 van ons reeds een Raspberry Pi bezitten, 
en er dus al een beetje bekend met waren.
Wat we uiteindelijk moesten bereiken was een "vervolg" op een project dat werd gedaan door studenten
van het vorige jaar. We moesten dus beginnen met het recreeeren van hun project en bevindingen.
Onze setup was het eerstvolgende dat we moesten verzinnen. We hadden eerst een kleine USB dongle aan de
Raspberry Pi aangesloten. De vorige studenten hadden ons hier echter reeds voor gewaarschuwd in hun verslag: 
er zijn functionaliteiten die de dongle niet bezit om te kunnen verbinden met het WPA2 enterprise netwerk
van de campus. We hebben dus geopteerd voor de AWUS036H, waarvan er enkelen door de school werden aangeboden voor
gebruik in projecten. 
Een access point hebben we van thuis meegenomen. We hebben dan alles op het kot van Michiel geinstalleerd. Zo konden we alledrie de Pi via ssh besturen vanuit welke plek dan ook, zonder dat we met iemand rekening moesten houden (we zijn voor het gemak wel het vaakst bij Michiel samengekomen). 
Nadat we de oude scriptjes een beetje hadden geupdatet konden we aan de slag met nieuwe functionaliteiten. 
Ons voornamelijk doel was een autonoom toestel: bij het opstarten van de pi scant hij automatisch access points
in de buurt, en zal proberen de paswoorden te kraken. Als hij dan de WEP-key van een AP heeft gevonden verbindt
hij er automatisch ook mee. Als dit gebeurd is wordt alle data doorgemaild (naar Michiel Mulder (s079157@ap.be)), o.a. de netwerkanalyse van nmap, die om de paar minuten opnieuw ook wordt uitgevoerd.
Ons toestel kan dus worden toegepast om de WEP-keys te verzamelen, en werkt op verschillende access points.

We zetten raspbian op de raspberry en vliegen erin.

##Setup
![Setup1](http://i.imgur.com/PxWgfbi.jpg?1)

We maken gebruik van een raspberry pi als core van het project (linksboven), de AWUS036H wifi-dongle (linksonder) en een SNB6500 als doelwit (rechts). 


##Startup

We beginnen alvast met een initiele mail die het ip-address geeft van de raspberry in het huidige aangesloten netwerk. Dit benutten we om via ssh verbinding. Om dit te verwezelijken gebruiken we het script **mailme.py** uit voorgaand project en zetten dit in de ***rc.local*** file. <br/> ***rc.local*** is een bestand dat wordt aangeroepen bij aanvang van het bootproces en is dus ideaal om processen mee te starten bij het opstarten. Omdat deze nauw bij het bootproces ligt kan deze geen errors verdragen. Hierdoor is deze best fragiel en niet gemakkelijk te hanteren.

##Wifite

Om een netwerk aan te kunnen vallen moeten we eerst een netwerk hebben waarop we onze attacks kunnen loslaten. Hiervoor runnen we *[wifite](https://code.google.com/p/wifite/)*, die een aantal tools combineert om een bruteforce attack uit te voeren. We doen dit  parallel met het voorgaande project aan de hand van een rainbowlist (*rockyou.txt*-bestand), omdat dit tijd bespaart. Een bruteforce-attack kan lang duren zonder en zeker op wpa-beveiligde netwerken. <br/> We starten *wifite*:

		$ sudo /home/pi/reaver-1.4/src/wifite.py -i mon0 -all -wep 
				-dict /pentest/passwords/wordlists/rockyou.txt -aircrack > /home/pi/reaver-1.4/src/log.txt

Indien we alle access points in de buurt willen vinden, ongeacht de beveiliging, gebruiken we deze command zonder "-wep". Ook kunnen we instellen dat we enkel access points vanaf bijvoorbeeld 50 dB of meer willen waarnemen door "-pow 50". In het laatste deel van bovenstaande command wordt de log weggeschreven naar het bestand **log.txt**. In dit tekstbestand kunnen we  Dit wordt via mail doorgestuurd met **mailLog.py** uit voorgaand project.

		$ sudo /home/pi/reaver-1.4/src/wifite.py -i mon0 -all -pow 50 
				-dict /pentest/passwords/wordlists/rockyou.txt

Om deze vlot te laten opstarten hebben we enkele aanpassingen moeten toepassen alvorens dit te runnen. De *network manager* wilt onze interfaces graag monitoren. Hierdoor kan *wifite* zichzelf niet gemakkelijk in monitormode zetten - dit komt van pas als we alles geautomatiseerd willen laten verlopen.

		$ sudo /etc/init.d/network-manager stop

Wanneer *wifite* een access point heeft kunnen kraken zal deze het *mac-address*, de *SSID*, de *gebruikte beveiliging* en het *wachtwoord * opslaan in een **cracked.csv** bestand.

##wifiConnect.py

Nadat *wifite* de nodige accespoints heeft kunnen kraken willen we de verzamelde informatie gebruiken. De *SSID* en het *wachtwoord* kunnen we gebruiken om de raspberry via de wifi-dongle te verbinden met de gekraakte wifi. Dit gebeurt via het zelfgemaakte **wifiConnect.py** script.

		$ sudo python wifiConnect.py

Op het einde van het **wifiConnect.py**-script zenden we het **cracked.csv** bestand eveneens naar het gebruikte e-mail adres aan de hand van **mailCracked.py**, gebaseerd op de scripts gebruikt in voorgaand project. <br/> Als we hier naar de netwerkinterfaces kijken, zien we dat *wlan0* (of een eventuele andere gebruikte wireless interface) geconfigureerd is met een ip-adress en alles wat we nodig hebben om een wireless verbinding tot stand te brengen.

##automailer.sh

Dit shellscript hebben we samengesteld om informatie te verzamelen over het nieuwe netwerk waar we onszelf mee verbonden hebben. We doen dit aan de hand van de tool **nmap**, waarbij we gaan zoeken naar open poorten *'--open'*, de *operating systems* *'-O'* en alle gebruikte ip adressen binnen het subnet op desbetreffende accesspoint. Verder wordt de output naar **output.txt** weggeschreven, dat vervolgens gebruikt wordt om doorgestuurd te worden naar het gebruikte e-mail addres. Ook hier wordt een python-bestand gebruikt, gebaseerd op de mailscripts uit voorgaand project.

		$ sudo nmap --open -O 192.168.0.*/24 192.168.1.*/24 > output.txt
		$ cd ~/Documents/PenPiScripts/
		$ sudo python mailnmap.py

##rc.local

![rc.localImg](http://i.imgur.com/hVRhhEt.png?1)


Om van al deze scripts een geheel te maken en de raspberry als zelfstandige tool te laten runnen, gebruiken we het **rc.local** bestand. Zoals reeds vermeld is dit een bestand dat in raspbian gebruikt wordt bij bootup. Dit is dus de perfecte locatie om de files in gang te zetten en te monitoren. <br/> Om de de nodige files te in het oog te houden gebruiken we een shellscript [**watch.sh**](https://gist.github.com/mikesmullin/6401258), van op github. Dit shellscript neemt een eerste parameter aan die wordt aangeduid als te monitoren bestand. Een tweede parameter zorgt voor een actie indien er in het bestand uit de eerste parameter een verandering is gebeurd. <br/> Bij het gebruiken van **rc.local** moeten we goed in het achterhoofd houden dat het gebruikt wordt kort bij het boot proces. Ter herhaling, dit wil zeggen dat er geen errors binnen **rc.local** mogen voorkomen, omdat deze niet weet hoe ze af te handelen. Dit is een struikelblok.

<br/>
<br/>
<br/>

#Conclusie
We hebben ons in dit project voor de eerste facetten dus gebaseerd op het voorgaande PenPi project. Dit is om van start te gaan een degelijke hulp geweest om gevoel te krijgen binnen raspbian en met de tools die we nodig hadden om het geheel te verwezelijken. Toch verliep het niet helemaal van een leien dakje. Dit was vooral te wijten aan nieuwere versies zoals wifite en compatibiliteiten met bepaalde scripts. Deze errors konden we uiteindelijk weg-troubleshooten met opzoekwerk. Algemeen zijn we zelf tevreden met de mijlpalen die we bereikt hebben, hoewel we de PenPi 2.0 toch graag volledig autonoom hadden zien werken. Dit hebben we niet volledig kunnen bereiken aangezien een target access point vaak niet geconfigureerd is om netwerkverkeer buiten het netwerk te laten. Zo kregen we bijvoorbeeld een ip-adress wel binnen nadat de PenPi 2.0 de SNB6500 access point had gekraakt, maar konden we geen ssh-verbinding opstellen. Dit kom dus door de configuratie op de acces point die de ssh niet toelaat. Als we geen verbinding kunnen opstellen kunnen we deze instellingen dus ook niet meteen manipuleren. Desalniettemin hebben we de PenPi 2.0 zo sterk mogelijk op punt gesteld.

<br/>
<br/>
<br/>
<br/>
<br/>

###Extra
[Afbeeldingen](http://imgur.com/a/B0NFs)

[Video](https://vid.me/rszB)

[Wifite 1](https://code.google.com/p/wifite/)

[Wifite 2](http://resources.infosecinstitute.com/wifite-walkthrough-part-1/)

[rc.local](https://www.raspberrypi.org/documentation/linux/usage/rc-local.md)

[nmap](http://www.cyberciti.biz/networking/nmap-command-examples-tutorials/)

[watch.sh](https://gist.github.com/mikesmullin/6401258)s