#!/usr/bin/python
import re
import serial 
import json
import time
from time import sleep
from json import dumps
from kafka import KafkaProducer
from serial import Serial
from datetime import datetime
from json import json_util

# Data definitions
ser = serial.Serial('/dev/ttyUSB0', 9600)
producer = KafkaProducer(bootstrap_servers=['10.194.24.26:9092'],
						 value_serializer=lambda x:dumps(x).encode('utf-8'))
topic = 'numtest'

# We send the user's information with the date to create a specific stream
date = datetime.now()
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
user_dict = {'username': currentuser, 'password': user_password, stream_date:
				date_time}

producer.send('numtest', json.dumps(user_dict,
				 default=json_util.default).encode('utf-8'))


# loop
while True:
    data = ser.readline()
    if data:
        print(data)
        data = re.sub('\r |\n','',data)
        producer.send('numtest', data, 
        				timestamp_ms = lambda: int(round(time.time()*1000)))
        sleep(2)