 
#Send messages to specific partition

from time import sleep
from json import dumps
from kafka import KafkaProducer

topic_name='consumer-group-topic'
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))

 
while True:
    message = input("Enter message to transmit")
    partition_num = int(input("Enter partition number to push message to"))
    producer.send(topic_name, value=message, partition=partition_num)

producer.flush()
producer.close()