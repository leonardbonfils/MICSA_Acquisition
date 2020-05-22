none#!/usr/bin/python
import re
import serial 
import json
import time
from time import sleep
from json import dumps
from kafka import KafkaProducer

# Definition des donnees
ser = serial.Serial('/dev/ttyUSB0', 9600)
producer = KafkaProducer(bootstrap_servers=['10.194.24.26:9092'], value_serializer=lambda x:dumps(x).encode('utf-8'))
topic = 'numtest'


# On envoie en premier les infos de usagé et les informations de la série de données: date, heure et secondes.


# Boucle
while True:
    data = ser.readline()
    if data:
        print(data)
        data = re.sub('\r |\n','',data)
        producer.send('numtest', data_numbers_only)
        sleep(2)

  

