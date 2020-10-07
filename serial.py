"""#!/usr/bin/python"""
#!C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.7_3.7.2032.0_x64__qbz5n2kfra8p0

# ------------------------------ Script Kafka Producer ------------------------------- #
# -------------------------- Club SynapsETS - MICSA Project -------------------------- #

# Libraries
import serial
import string
import sys
import time
from json import dumps
from json import loads
from time import sleep
from kafka import KafkaProducer
from kafka import KafkaConsumer
from datetime import datetime

# Connection parameters
ser = serial.Serial('/dev/ttyUSB0', 9600)
serverIP = ['10.194.24.26:9092']
client_id = 'rasPi'
producerTopic = 'micsaData'
consumerTopic = 'micsaAuth'
consumerGroup = 'pythonScript'
request_timeout = 3

# Consumer data
consUser = ""
consPW = ""
consSeriesID = 0
consAuth = False

# Program variables
now = None              # Current date and time
user = f"{sys.argv[1]}" # First program argument
pw   = f"{sys.argv[2]}" # Second program argument

# ------------------------------------------------------------------------------------ #
# ------------------------------- Producer definition -------------------------------- #
# ------------------------------------------------------------------------------------ #

producer = KafkaProducer( \
    bootstrap_servers=serverIP, \
    value_serializer=lambda x: dumps(x).encode('utf-8'))

# ------------------------------------------------------------------------------------ #
# ------------------------------- Consumer definition -------------------------------- #
# ------------------------------------------------------------------------------------ #

consumer = KafkaConsumer(consumerTopic, \
    group_id=consumerGroup, \
    bootstrap_servers=serverIP, \
    value_deserializer=lambda x: loads(x).decode ('utf-8'))

# ------------------------------------------------------------------------------------ #
# -------------------------- Send authentification request --------------------------- #
# ------------------------------------------------------------------------------------ #

# Envoyer un premier message avec user, pw (doit être crypté) et id de la série donnée #

# On utilise une ID de série aléatoire 
randomSeriesID = 19584923584923
seriesID = f"{randomSeriesID}"

# Initialisation date actuelle
update_date()

# On crée le JSON qui contient tous les paramètres d'identification
authJSON = { 'username': user,
        'password' : pw,
        'seriesID' : seriesID,
        'date' : now }

authAttempt = producer.send(producerTopic, authJSON)
result = authAttempt.get(timeout=request_timeout)
producer.flush()

# ------------------------------------------------------------------------------------ #
# ------------------------- Receive authentification results ------------------------- #
# ------------------------------------------------------------------------------------ #

# Recevoir les résultats d'authentification et les traiter
for authMsg in consumer:
    consUser = authMsg.username
    consPW = authMsg.password
    consSeriesID = authMsg.seriesID
    consAuth = authMsg.result
    
    print("user: %s, password: %s, seriesID: %d, authentification success: %r"\
        % (authMsg.username, authMsg.password, authMsg.seriesID, authMsg.result))

# ------------------------------------------------------------------------------------ #
# -------------------- Transmit a "series ID + serial data" combo -------------------- #
# ------------------------------------------------------------------------------------ #

# Mettre à jour la date
update_date()

# Envoyer les données
while True:
    data = ser.readline()
    if data:
        print(data)
        data = data.replace('\r','').replace('\n','')
        dataJSON = { 'seriesID' : seriesID, # Il faut qu'on génère des seriesID aléatoires avec une fonction
                'date' : now, 
                'data' : data }
        attempt = producer.send(producerTopic, dataJSON)
        result = attempt.get(timeout=request_timeout)
        producer.flush()
        sleep(2)

# ------------------------------------------------------------------------------------ #
# ----------------------------- Close Kafka connections ------------------------------ #
# ------------------------------------------------------------------------------------ #

# Close the consumer
consumer.close()

# Close the producer
producer.close()

# ------------------------------------------------------------------------------------ #
# ------------------------------- Auxiliary functions -------------------------------- #
# ------------------------------------------------------------------------------------ #

def update_date():
    now = datetime.now()
    date = now.strftime("%d/%m/%Y, %H:%M:%S")

# ------------------------------------------------------------------------------------ #
# ---------------------------------- End of script ----------------------------------- #
# ------------------------------------------------------------------------------------ #

# ------------------------------------------------------------------------------------ #
# --------------------------- Example consumer reception ----------------------------- #
# ------------------------------------------------------------------------------------ #

for message in consumer:
    print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,\
        message.offset, message.key, message.value))

# ------------------------------------------------------------------------------------ #
# -------------------------- Example producer transmission --------------------------- #
# ------------------------------------------------------------------------------------ #

# Producer data transmission - serial data
while True:
    data = ser.readline()
    if data:
        print(data)
        data = data.replace('\r','').replace('\n','')
        attempt = producer.send(producerTopic, b'data')
        result = attempt.get(timeout=request_timeout)
        producer.flush()
        sleep(2)
