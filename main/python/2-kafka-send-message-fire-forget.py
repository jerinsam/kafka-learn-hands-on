 
#Fire-and-forget

from time import sleep
from json import dumps
from kafka import KafkaProducer

# Create topic using below script
# kafka-topics --create --topic test-message-sending-method --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1

topic_name='test-message-sending-method'
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))

for e in range(100):
    data = {'number' : e}
    print(data)
    producer.send(topic_name, value=data)
    sleep(0.5)

producer.flush()
producer.close()