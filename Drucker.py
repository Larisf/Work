#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import signal
import subprocess
import RPi.GPIO as GPIO
import time
import sys
import os

#Signal-Handler Methode zum Beenden des Programmes mit STRG+C
def signal_handler(sig, frame):
   print("\nCongratz, you fucked up...")										#Ausgabe bei Beendigung mit Strg+C
   GPIO.cleanup()													#GPIO pins zurücksetzen
   etikett.close()													#Datei für das Etikett schließen
   log.close()														#Log-Datei schließen
   sys.exit(0)														#Programm beenden

#GPIO setzen zum Empfangen des Druckauftrages
GPIO.setmode(GPIO.BCM)													#Das Pin-Schema des Broadcom-Chips verwenden
GPIO.setup(21, GPIO.IN,pull_up_down = GPIO.PUD_DOWN)									#Pin 21 als Eingang setzen mit integriertem Pull_Down (gegen Masse)
GPIO.add_event_detect(21, GPIO.RISING, bouncetime = 1500)								#Softwareseitige Entprellung für 1 Sekunde
GPIO.setup(20, GPIO.OUT)												#Pin 20 als Ausgang setzen
GPIO.output(20,1)													#Pin 20 auf HIGH setzen
#Variablen
ID_Nr = "AS3 2701-3200 STE"												#ID_Nr vom Verteiler(Muss angepasst werden!)
datei_druck = "Pruefstation/Etikett.txt"										#Name der Datei, die gedruckt werden soll
drucker_name = "Zebra-TLP2844"												#Name der unter printers angezeigt wird
anzahlNummer = 1
drucken = 0														#Variable zur Abfrageüberprüfung, ob gedruckt werden darf, oder nicht

#Hauptprogramm
while True:
	tag = time.strftime("%d.%m.%Y")											#Formatiertes Datum als Tag,Monat,Jahr
	uhrzeit = time.strftime("%H:%M:%S")										#Formatierte Uhrzeit Stunden,Minuten,Sekunden
	datei_log = "Pruefstation/Log_Files/"+tag+".log"								#Variable für die Log-Datei - Täglich eine neue
   	signalA = GPIO.input(21)											#Eingang abfragen und in eine Variable schreiben
   	signal.signal(signal.SIGINT, signal_handler)									#Methode für die Bearbeitung bei STRG+C aufrufen
   	if signalA == GPIO.HIGH and drucken == 0:									#Abfrage, ob der Eingang auf HIGH ist und keine Druckerfreigabe vorliegt
	   	etikett = open(datei_druck,"w")										#Datei zum Druck öffnen
		log = open(datei_log,"a")										#Log-Datei öffnen
		drucken =  1												#Druckerfreigabevariable setzen
		log.write("ZS: "+str(anzahlNummer)+" | "+tag+"-"+uhrzeit+" - Prüfung bestanden\n")			#In die Log-Datei schreiben
		log.close()												#Log-Datei schließen
		etikett.write("Qualitäts- und Funktionsprüfung\nSTW-Verteiler, ID-Nr:"+ID_Nr)				#In die Druck-Datei schreiben
		etikett.write("\nBaugruppe PIN 1-15 geprüft und Funktion erfolgreich getestet")				#
		etikett.write("\n\n\nDatum: \t"+ tag+"\n\n\nUhrzeit: "+ uhrzeit+"\t\t\tZS:\t"+ str(anzahlNummer))	#
      		anzahlNummer += 1											#Laufvariable erhöhen
 	  	etikett.close()												#Druck-Datei schließen
   	if drucken == 1 and signalA == GPIO.LOW:									#Abfrage ob die Druckerfreigabe gegeben ist und das Eingangssignal auf LOW ist
		os.system("lpr -P  "+drucker_name+" "+ datei_druck) 							#Befehl an das System zum Drucken
      		drucken = 0												#Druckerfreigabe nach dem Druck auf LOW setzen

