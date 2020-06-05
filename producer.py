"""#!/usr/bin/python"""
#!C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.7_3.7.2032.0_x64__qbz5n2kfra8p0

# ------------------------------ Script Kafka Producer ------------------------------- #
# -------------------------- Club SynapsETS - MICSA Project -------------------------- #

# Libraries
import serial
import string
from json import dumps
from time import sleep
from kafka import KafkaProducer

# Parameters
ser = serial.Serial('/dev/ttyUSB0', 9600)
serverIP = ['10.194.24.26:9092']
client_id = 'rasPi'
topic = 'numtest'
request_timeout = 3

# ------------------------------------------------------------------------------------ #
# ------------------------------- Producer definition -------------------------------- #
# ------------------------------------------------------------------------------------ #

# Producer definition
producer = KafkaProducer( \
    bootstrap_servers=serverIP, \
    value_serializer=lambda x:dumps(x).encode('utf-8'))

# ------------------------------------------------------------------------------------ #
# ------------------------------ Producer transmission ------------------------------- #
# ------------------------------------------------------------------------------------ #

# Producer data transmission - serial data
while True:
    data = ser.readline()
    if data:
        print(data)
        data = data.replace('\r','').replace('\n','')
        attempt = producer.send(topic, b'data')
        result = attempt.get(timeout=request_timeout)
        producer.flush()
        sleep(2)


# Close the producer
producer.close()

# ------------------------------------------------------------------------------------ #
# ---------------------------------- End of script ----------------------------------- #
# ------------------------------------------------------------------------------------ #