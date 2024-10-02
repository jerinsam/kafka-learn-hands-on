# Start Zookeeper and Broker
# Create Topic
# Code for customized partitioner

from time import sleep
from json import dumps
from kafka import KafkaProducer

topic_name='index-file-topic'
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))

for e in range(1000):
    data = {'number' : e}
    print(data)
    producer.send(topic_name, value=data)
    sleep(0.0002)

producer.flush()
producer.close()