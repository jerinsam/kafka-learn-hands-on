from kafka import KafkaConsumer
import json

# Script to create topic
# kafka-topics --create --topic initial-commit-topic --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1

topic_name='initial-commit-topic'

# intial offset is managed by property "auto_offset_reset", once offset is committed then this property will be ignored and consumer will start consuming from the committed offset 

consumer = KafkaConsumer( 'initial-commit-topic', bootstrap_servers = 'localhost:9092', 
value_deserializer=lambda m: json.loads(m.decode('utf-8')),auto_offset_reset='earliest' , group_id='lmn-consumer-grp-abcd' 
)

print(consumer)

for message in consumer: #For loop automatically manages the Polling
    print(message) 