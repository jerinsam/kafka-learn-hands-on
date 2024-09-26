from kafka import KafkaConsumer

# TopicPartition and OffsetAndMetadata is required to manually commit offset
from kafka import TopicPartition , OffsetAndMetadata


import json

# Script to create topic
# kafka-topics --create --topic exactly-once-topic --bootstrap-server localhost:9092 --replication-factor 1 --partitions 2

topic_name='exactly-once-topic'

'''
Start with 1 consumer and then create another consumer in the same consumer group, to understand 
how consumer rebalancing happens when a new consumer from same consumer group starts accepting message
'''

consumer = KafkaConsumer (topic_name, bootstrap_servers = ['localhost:9092'],
value_deserializer=lambda m: json.loads(m.decode('utf-8')),group_id='demo112215sgtrjwrykvjh',auto_offset_reset='earliest',
                          enable_auto_commit =False)


for message in consumer: #For loop automatically manages the Polling

    # Message Processing Starts here

    print(message)
    print("The value is : {}".format(message.value))
    print("The key is : {}".format(message.key))
    print("The topic is : {}".format(message.topic))
    print("The partition is : {}".format(message.partition))
    print("The offset is : {}".format(message.offset))
    print("The timestamp is : {}".format(message.timestamp))

    # Manual Offset Commit - Exactly once Processing

    # TopicPartition takes 2 argument i.e. topic and partition
    tp=TopicPartition(message.topic,message.partition)

    # OffsetAndMetadata takes 2 argument i.e. offset + 1 and metedata (Timestamp is used here as metadata argument)
    # offset + 1: This tells Kafka the next message position to start from after the offset commit
    om = OffsetAndMetadata(message.offset+1, message.timestamp)

    print('TopicPartition is : {}'.format(tp))
    print('OffsetAndMetadata is : {}'.format(om))

    # Manually Commit Offset
    consumer.commit({tp:om})
    print('*' * 100)