#!/usr/bin/python
import serial 
import json
import time
from kafka import KafkaProducer

# Definition des donnees
ser = serial.Serial('/dev/ttyUSB0', 9600)
#producer = KafkaProducer(bootstrap_servers='localhost:9062', request_timeout_ms=10000)
topic = 'micsa_data'

# Boucle
while True:
    #time.sleep(3)
    data = ser.readline()
    if data:
        print(data)
        data=None
        #producer.send(b'')
