
##### Partition Assignment Example - Consumer 2

from kafka.coordinator.assignors.range import RangePartitionAssignor
from kafka.coordinator.assignors.roundrobin import RoundRobinPartitionAssignor

from kafka import KafkaConsumer
from kafka import TopicPartition , OffsetAndMetadata
import kafka

import json

class MyConsumerRebalanceListener(kafka.ConsumerRebalanceListener):


    def on_partitions_revoked(self, revoked):
        print("Partitions %s revoked" % revoked)
        print('*' * 50)

    def on_partitions_assigned(self, assigned):
        print("Partitions %s assigned" % assigned)
        print('*' * 50)

### Range Partition Assignor

consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                         group_id='demo112215sgtrjwrykvjh', auto_offset_reset='earliest',
                         enable_auto_commit=False,partition_assignment_strategy=[RangePartitionAssignor]
                         )

### Round Robin Partition Assignor

# consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],
#                          value_deserializer=lambda m: json.loads(m.decode('utf-8')),
#                          group_id='demo112215sgtrjwrykvjh', auto_offset_reset='earliest',
#                          enable_auto_commit=False,partition_assignment_strategy=[RoundRobinPartitionAssignor]
#                          )


## Listener Object
listener = MyConsumerRebalanceListener()

# Script to create topic
# kafka-topics --create --topic partition-assignment-topic --bootstrap-server localhost:9092 --replication-factor 1 --partitions 6

topic_name='partition-assignment-topic'

consumer.subscribe(topic_name,listener=listener)


for message in consumer:
    print(message)
    print("The value is : {}".format(message.value))
    tp=TopicPartition(message.topic,message.partition)
    om = OffsetAndMetadata(message.offset+1, message.timestamp)
    consumer.commit({tp:om})