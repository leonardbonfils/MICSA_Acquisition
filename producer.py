"""#!/usr/bin/python"""
#!C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.7_3.7.2032.0_x64__qbz5n2kfra8p0

# ------------------------------ Script Kafka Producer ------------------------------- #
# -------------------------- Club SynapsETS - MICSA Project -------------------------- #

# Libraries
import serial
import string
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

# Envoyer un premier message avec user, pw (crypté) et id de la série donnée #
# Réception d'un message du serveur Kafka (il faut faire un consumer) pour voir si l'identifiant est bon #
# Si c'est bon, on envoie un combo "id série donnée" + donnée de la série #

# ------------------------------------------------------------------------------------ #
# ------------------------------- Producer definition -------------------------------- #
# ------------------------------------------------------------------------------------ #

# Producer definition
producer = KafkaProducer( \
    bootstrap_servers=serverIP, \
    value_serializer=lambda x:dumps(x).encode('utf-8'))

# ------------------------------------------------------------------------------------ #
# ------------------------------- Consumer definition -------------------------------- #
# ------------------------------------------------------------------------------------ #

consumer = KafkaConsumer(consumerTopic, \
    group_id=consumerGroup, \
    bootstrap_servers=serverIP, \
    value_deserializer=lambda x: json.loads(x.decode ('utf-8')))

# ------------------------------------------------------------------------------------ #
# ------------------------------- Consumer reception --------------------------------- #
# ------------------------------------------------------------------------------------ #

for message in consumer:
    print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,\
        message.offset, message.key, message.value))

# ------------------------------------------------------------------------------------ #
# ------------------------------ Producer transmission ------------------------------- #
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


# Close the producer
producer.close()

# ------------------------------------------------------------------------------------ #
# ---------------------------------- End of script ----------------------------------- #
# ------------------------------------------------------------------------------------ #