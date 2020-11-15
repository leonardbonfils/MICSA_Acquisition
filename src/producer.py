#!/usr/bin/python
import serial
import time
from time import sleep
from kafka import KafkaProducer

# Definition des donnees
# USB source is "/dev/ttyUSB0" when using custom circuit and "/dev/ttyACMX" (X is number, depends on port used) for Myoware circuit with arduino
ser = serial.Serial('/dev/ttyACM0')
ser.flushInput()
producer = KafkaProducer(bootstrap_servers=['10.194.24.26:9092'])
topic = 'micsaData'


# On envoie en premier les infos de usagé et les informations de la série de données: date, heure et secondes.


# Boucle
while True:
	try:
	    data = ser.readline()
	    if data:
	    	data = data.rstrip(b'\r\n')
	    	print(data)
	    	producer.send(topic, data)
	except:
		print("Error read")


