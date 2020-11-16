from kafka import KafkaProducer
from json import dumps
from random import randint, random
from time import sleep

topic = 'micsaData'

options = {
    'bootstrap_servers'      : '10.194.24.26:9092',
    'enable_auto_commit'     : True,
    'auto_commit_interval_ms': 5000,
    'fetch_max_wait_ms'      : 100,
    'fetch_min_bytes'        : 1,
    'fetch_max_bytes'        : 1024 * 1024
}

producer = KafkaProducer(bootstrap_servers=['10.194.24.26:9092'], value_serializer=lambda x:dumps(x).encode('utf-8'))

changeData = randint(200, 500)
count = 0
base = 2
while True:
    if (count >= changeData):
        count = 0
        if base == 4:
            changeData = randint(200, 500)
            base = 2
        else:
            changeData = randint(100, 200)
            base = 4
    count += 1
    data = round(random() + base, 1)

    print(data)
    producer.send(topic, data)
    sleep(0.1)