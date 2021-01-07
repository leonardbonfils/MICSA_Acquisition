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
from Cryptodome.Cipher import AES
import base64
import os
import platform
import random

# Connection parameters
#define AUTHENTIFIACTION_SUCCESSFUL 1
#define AUTHENTIFICATION_FAILURE 0

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
# ------------------------------- Auxiliary functions -------------------------------- #
# ------------------------------------------------------------------------------------ #

def update_date():
    now = datetime.now()
    date = now.strftime("%d/%m/%Y, %H:%M:%S")
    return date

def encryptionInfo(privateInfo):
    BS = 16
    PADDING = '{'
    pad = lambda s: bytes(s + (BS - len(s) % BS) * PADDING, 'utf-8')
    EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
    secret = os.urandom(BS)
    print ('Encryption key:', secret)
    cipher = AES.new(secret, AES.MODE_ECB)
    encoded = EncodeAES(cipher, privateInfo)
    print ('Encrypted string:', encoded)
    return encoded.decode("utf-8")

def hasSerialData():
    if platform.system() == 'Linux':
        return True
    else:
        return False

def hasSerialData():
    import serial
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    ser.flushInput()

# Connection parameters
#define AUTHENTIFICATION_SUCCESSFUL 1
#define AUTHENTIFICATION_FAILURE 0

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

# Envoyer un premier message avec user, pw (doit etre crypte) et id de la serie donnee #

# On utilise une ID de serie aleatoire
randomSeriesID = random.randint(0,9999999)
seriesID = f"{randomSeriesID}"

# Initialisation date actuelle
update_date()

# On cree le JSON qui contient tous les parametres d'identification
encryptedPW = encryptionInfo(pw)
authJSON = { 'username': user,
        'password' : encryptedPW,
        'seriesID' : seriesID,
        'date' : update_date() }

authAttempt = producer.send(producerTopic, authJSON)
result = authAttempt.get(timeout=request_timeout)
producer.flush()

# ------------------------------------------------------------------------------------ #
# ------------------------- Receive authentification results ------------------------- #
# ------------------------------------------------------------------------------------ #

print("\nNow treating authentification\n")
# Recevoir les resultats d'authentification et les traiter
# for authMsg in consumer:
#     consUser = authMsg.username
#     consEncryptedPW = authMsg.password
#     consSeriesID = authMsg.seriesID
#     consAuth = authMsg.result
#      
#     print("user: %s, password: %s, seriesID: %d, authentification success: %r"\
#         % (authMsg.username, authMsg.password, authMsg.seriesID, authMsg.result))

# ------------------------------------------------------------------------------------ #
# -------------------- Transmit a "series ID + serial data" combo -------------------- #
# ------------------------------------------------------------------------------------ #

print("\nNow sending data to kafka broker")

# Envoyer les donnees
while True:
    data = ser.readline()
    print("Read one line\n")
    if hasSerialData():
        data = ser.readline()
    else:
        data = b'0000'
    if data:
        data = data.rstrip(b'\r\n')
        data = data.decode("utf-8")
        print(data)
        
        # Mettre a jour la date
        dataJSON = { 'seriesID' : seriesID,
                'date' : update_date(),
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
# ---------------------------------- End of script ----------------------------------- #
# ------------------------------------------------------------------------------------ #
