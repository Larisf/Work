#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import signal
import subprocess
import RPi.GPIO as GPIO
import time
import sys
import os

#GPIO setzen zum Empfangen des Druckauftrages
GPIO.setmode(GPIO.BCM)															#Das Pin-Schema des Broadcom-Chips verwenden
GPIO.setup(21, GPIO.IN)															#Pin 21 als Eingang setzen
GPIO.setup(20, GPIO.OUT)														#Pin 20 als Ausgang setzen
GPIO.output(20,1)															#Pin 20 auf HIGH setzen

#Variablen
ID_Nr = "AS3 2701-3200 STE"														#ID_Nr vom Verteiler(Muss angepasst werden!)
datei_druck = "Pruefstation/Etikett.txt"												#Name der Datei, die gedruckt werden soll
drucker_name = "Zebra-TLP2844"														#Name der unter printers angezeigt wird
anzahlNummer = 1
i = 0																	#unnütze Variable															

#Methode für das einkommende Signal
def dataWritePrint(channel):
	global ID_Nr
	global datei_druck
	global drucker_name
	global anzahlNummer
	if GPIO.input(21) == 0:														#Eingang abfragen
		tag = time.strftime("%d.%m.%Y")												#Formatiertes Datum als Tag,Monat,Jahr
		uhrzeit = time.strftime("%H:%M:%S")											#Formatierte Uhrzeit Stunden,Minuten,Sekunden
		datei_log = "Pruefstation/Log_Files/"+tag+".log"									#Variable für die Log-Datei - Täglich eine neue
		etikett = open(datei_druck,"w")												#Datei zum Druck öffnen
		log = open(datei_log,"a")												#Log-Datei öffnen
		log.write("ZS: "+str(anzahlNummer)+" | "+tag+"-"+uhrzeit+" - Prüfung bestanden\n")					#In die Log-Datei schreiben
		log.close()														#Log-Datei schließen
		etikett.write("Qualitäts- und Funktionsprüfung\nSTW-Verteiler, ID-Nr:"+ID_Nr)						#In die Druck-Datei schreiben
		etikett.write("\nBaugruppe PIN 1-15 geprüft und Funktion erfolgreich getestet")						#
		etikett.write("\n\n\nDatum: \t"+ tag+"\n\n\nUhrzeit: "+ uhrzeit+"\t\t\tZS:\t"+ str(anzahlNummer))			#
      		anzahlNummer += 1													#Laufvariable erhöhen
 		etikett.close()														#Druck-Datei schließen
	else:
		os.system("lpr -P  "+drucker_name+" "+ datei_druck) 									#Befehl an das System zum Drucken

GPIO.add_event_detect(21, GPIO.BOTH, callback = dataWritePrint, bouncetime = 1000)							#Auf Flanke reagieren
   		
#Hauptprogramm
try:
	while True:
		i += 1
		i -= 1
except KeyboardInterrupt:
	GPIO.cleanup()															#GPIO pins zurücksetzen
   	etikett.close()															#Datei für das Etikett schließen
   	log.close()															#Log-Datei schließen
	print("\nCongratz, you fucked up...")												#Ausgabe bei Beendigung mit Strg+C
 
