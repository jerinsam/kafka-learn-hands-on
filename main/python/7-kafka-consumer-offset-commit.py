from kafka import KafkaConsumer
import json

# Script to create topic
# kafka-topics --create --topic initial-commit-topic --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1

topic_name='initial-commit-topic'

consumer = KafkaConsumer( 'initial-commit-topic', bootstrap_servers = 'localhost:9092', 
value_deserializer=lambda m: json.loads(m.decode('utf-8')),auto_offset_reset='earliest' , group_id='lmn-consumer-grp-abcd',
enable_auto_commit = True, auto_commit_interval_ms = 3000
)

print(consumer)

for message in consumer:
    print(message) 