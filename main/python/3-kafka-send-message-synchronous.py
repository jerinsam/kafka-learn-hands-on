 
# Synchronous send

from time import sleep
from json import dumps
from kafka import KafkaProducer


# Create topic using below script
# kafka-topics --create --topic test-message-sending-method --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1

topic_name='test-message-sending-method'

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))

for e in range(5):
    data = {'number' : e}
    print(data)
    try:
        record_metadata =producer.send(topic_name, value=data).get(timeout=10)
        print(type(record_metadata)) ##kafka.producer.future.RecordMetadata : future record
        print(record_metadata)
        print(record_metadata.topic)
        print(record_metadata.partition)
        print(record_metadata.offset)
        sleep(0.5)
    except Exception as e:
        print(e)


producer.flush()
producer.close()
