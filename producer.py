"""#!/usr/bin/python"""
#!C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.7_3.7.2032.0_x64__qbz5n2kfra8p0

# ------------------------------ Script Kafka Producer ------------------------------- #
# -------------------------- Club SynapsETS - MICSA Project -------------------------- #

# Libraries
import serial
import string
import sys
from json import dumps
from json import loads
from time import sleep
from kafka import KafkaProducer
from kafka import KafkaConsumer

# Parameters
ser = serial.Serial('/dev/ttyUSB0', 9600)
serverIP = ['10.194.24.26:9092']
client_id = 'rasPi'
producerTopic = 'micsaData'
consumerTopic = 'micsaAuth'
consumerGroup = 'pythonScript'
request_timeout = 3

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
    value_deserializer=lambda x: loads(x.decode ('utf-8')))

# ------------------------------------------------------------------------------------ #
# -------------------------- Send authentification request --------------------------- #
# ------------------------------------------------------------------------------------ #
# Envoyer un premier message avec user, pw (doit être crypté) et id de la série donnée #
# Utilisation des deux arguments passés au programme Python
user = f"{sys.argv[1]}"
pw   = f"{sys.argv[2]}"

# On utilise une ID de série aléatoire 
randomSeriesID = 19584923584923
seriesID = f"{randomSeriesValue}"

# On crée le JSON qui contient tous les paramètres d'identification
authJSON = { 'username': user,
        'password' : pw,
        'seriesID' : seriesID }

authAttempt = producer.send(producerTopic, authJSON)
result = authAttempt.get(timeout=request_timeout)
producer.flush()

# ------------------------------------------------------------------------------------ #
# ------------------------- Receive authentification results ------------------------- #
# ------------------------------------------------------------------------------------ #

# ------------------------------------------------------------------------------------ #
# -------------------- Transmit a "series ID + serial data" combo -------------------- #
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