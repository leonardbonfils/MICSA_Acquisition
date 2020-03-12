from kafka import kafkaConsumer
from pymongo import MongoClient
from json import loads


consumer = kafkaConsumer('micsa_data',bootstrap_servers=['localhost:9092'],auto_offset_reset ='earliest',enable_auto_commit=1ms, group_id='my-group')

client = MongoClient('localhost:27017')
collection = client.micsa_data.micsa_data
