
##### Partition Assignment Example - Consumer 2

from kafka.coordinator.assignors.range import RangePartitionAssignor
from kafka.coordinator.assignors.roundrobin import RoundRobinPartitionAssignor

from kafka import KafkaConsumer
from kafka import TopicPartition , OffsetAndMetadata
import kafka
import json
from time import sleep

### Range Partition Assignor

consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                         group_id='demo-consumer-group', auto_offset_reset='latest',
                         enable_auto_commit=False)
 

# Script to create topic
# kafka-topics --create --topic consumer-lag-topic --bootstrap-server localhost:9092 --replication-factor 1 --partitions 2

topic_name='consumer-lag-topic'

consumer.subscribe(topic_name)



for message in consumer:
    print(message)
    print("The value is : {}".format(message.value))
    tp=TopicPartition(message.topic,message.partition)
    om = OffsetAndMetadata(message.offset+1, message.timestamp)
    sleep(0.8) # This is used to mimic processing time taken by Consumer
    consumer.commit({tp:om})