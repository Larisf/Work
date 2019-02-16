#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
import RPi.GPIO as GPIO
import time
import os
import signal
 
#Define Pins
INPUT = 21                                                                                                          #Globalen Wert setzen, um bei Änderungen nur eine Zeile ändern zu müssen 
HIGH = 1                                                                                                            #Variable für den HIGH-Zustand definieren
LOW = 0
START = 20
 
#GPIO setzen zum Empfangen des Druckauftrages
GPIO.setmode(GPIO.BCM)                                                                                              #Das Pin-Schema des Broadcom-Chips verwenden
GPIO.setup(INPUT, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)                                                                                            #Pin 21 als Eingang setzen
GPIO.setup(START, GPIO.OUT)
GPIO.output(START, 0)
#Variablen
run = True
ID_Nr = "AS3 2701-3200 STE"                                                                                         #ID_Nr vom Verteiler(Muss angepasst werden!)
datei_druck = "Pruefstation/Etikett.txt"                                                                            #Name der Datei, die gedruckt werden soll
datei_log = "Pruefstation/Log_Files/"                                                                               #Pfad zu der Log-Datei
drucker_name = "Zebra-TLP2844"                                                                                      #Name der unter printers angezeigt wird
anzahlNummer = 1
drucker_freigabe = False
start_sys = 0
#Signahandler für das beenden des Progammes
def handler_stop_signal(signum, frame):
    global run
    run = False                                                                                                     #run auf False setzen, um die Schleife zu unterbrechen
    GPIO.cleanup()                                                                                                  #GPIOS zurücksetzen
    print("Programm beendet und GPIOS zurückgesetzt")
 
#Methode für das einkommende Signal
def dataWritePrint(channel):
    global ID_Nr
    global datei_druck
    global drucker_name
    global anzahlNummer
    global drucker_freigabe
    if GPIO.input(INPUT) == HIGH and drucker_freigabe == False:                                                     #Eingang abfragen
        tag = time.strftime("%d.%m.%Y")                                                                             #Formatiertes Datum als Tag,Monat,Jahr
        uhrzeit = time.strftime("%H:%M:%S")                                                                         #Formatierte Uhrzeit Stunden,Minuten,Sekunden
        with open(datei_log+tag+".log","a") as log:                                                                 #Log-Datei öffnen bzw. eine neue erstellen mit dem Datum
            log.write("ZS: "+str(anzahlNummer)+"\t| "+tag+"-"+uhrzeit+" - Prüfung bestanden\n")                     #In die Log-Datei schreiben
        log.close()                                                                                                 #Log-Datei schließen
        with open(datei_druck,"w") as etikett:                                                                      #Datei zum Druck öffnen
            etikett.write("Qualitäts- und Funktionsprüfung\nSTW-Verteiler, ID-Nr:"+ID_Nr)                           #In die Druck-Datei schreiben
            etikett.write("\nBaugruppe PIN 1-15 geprüft und Funktion erfolgreich getestet")                         #
            etikett.write("\n\n\nDatum: \t"+ tag+"\n\n\nUhrzeit: "+ uhrzeit+"\t\t\tZS:\t"+ str(anzahlNummer))       #
        etikett.close()                                                                                             #Druck-Datei schließen
            anzahlNummer += 1                                                                                       #Laufvariable erhöhen
        drucker_freigabe = True
        print("schreibe datei", GPIO.input(INPUT))
    else:
        time.sleep(1.5)
        if GPIO.input(INPUT) == LOW and drucker_freigabe == True:
            os.system("lpr -P  "+drucker_name+" "+ datei_druck)                                                     #Befehl an das System zum Drucken
            drucker_freigabe = False
            print("drucke")
#Auf Signale reagieren
GPIO.add_event_detect(INPUT, GPIO.BOTH, callback = dataWritePrint, bouncetime = 500)                                #Auf Flanke reagieren (RISING, FALLING, BOTH)
signal.signal(signal.SIGINT, handler_stop_signal)                                                                   #Auf Signale zum beenden des Programmes reagieren   
signal.signal(signal.SIGTERM, handler_stop_signal)                                                                  #
 
#Hauptprogramm
while run:                                                                                                          #Endlosschleife für das Programm, solange run = True ist
  if start_sys == 0:												    #Abfrage am Programmstart
    GPIO.output(START,1)
    start_sys = 1
    time.sleep(1.5)
  pass
