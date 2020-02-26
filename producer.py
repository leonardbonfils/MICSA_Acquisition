import serial 
import json
from kafka import KafkaProducer

# Définition des données
ser = serial.Serial('/dev/ttyUSB0', 9600)
#producer = KafkaProducer(bootstrap_servers='localhost:9062', request_timeout_ms=10000)
topic = 'micsa_data'

# Boucle
while True:
    data = ser.readline()
    if data:
        print(data)
        data=None
        #producer.send(b'')
