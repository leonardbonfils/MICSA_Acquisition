"""#!/usr/bin/python"""
#!C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.7_3.7.2032.0_x64__qbz5n2kfra8p0

# ------------------------------ Script Kafka Producer ------------------------------- #
# -------------------------- Club SynapsETS - MICSA Project -------------------------- #

# Libraries
import serial 
from json import dumps
from time import sleep
from kafka import KafkaProducer

# Parameters
#ser = serial.Serial('/dev/ttyUSB0', 9600)
serverIP = ['10.194.24.26:9092']
client_id = 'rasPi'
topic = 'micsaData'
retries = 5
request_timeout_ms = 10000

# ------------------------------------------------------------------------------------ #
# ------------------------------- Producer definition -------------------------------- #
# ------------------------------------------------------------------------------------ #

# Producer definition - very basic to run our initial tests
producer = KafkaProducer( \
    bootstrap_servers=serverIP, \
    value_serializer=lambda x:dumps(x).encode('utf-8'))

# Producer definition - full definition
"""
producer = KafkaProducer(\
    bootstrap_servers=serverIP,\
    client_id = client_id,\
    retries=retries,\
    value_serializer=lambda x:dumps(x).encode('utf-8'),\
    request_timeout_ms = request_timeout_ms,\
    )
"""

# ------------------------------------------------------------------------------------ #
# ------------------------------ Producer transmission ------------------------------- #
# ------------------------------------------------------------------------------------ #

# Producer data transmission - test data
for e in range(10):
    data = {'number' : e}
    attempt = producer.send('micsaData', value=data)
    result = attempt.get(timeout=60)
    producer.flush()
    sleep(0.1)
    print(e)

# Producer data transmission - serial data
"""
# Boucle
while True:
    data = ser.readline()
    if data:
        print(data)
        data=None
        producer.send(b'')
"""

# Close the producer
producer.close()

# ------------------------------------------------------------------------------------ #
# ---------------------------------- End of script ----------------------------------- #
# ------------------------------------------------------------------------------------ #