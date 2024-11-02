from kafka import KafkaConsumer
from kafka import TopicPartition , OffsetAndMetadata
from time import sleep
import json


# Script to create topic
# kafka-topics --create --topic consumer-lag-topic --bootstrap-server localhost:9092 --replication-factor 1 --partitions 2

topic_name='consumer-lag-topic'
group_id = "group-test-consumer-lag"
kafka_server='localhost:9092'
consumer = KafkaConsumer(topic,bootstrap_servers = [kafka_server],group_id=group_id)

# Get all partitions
partitions=consumer.partitions_for_topic(topic)
print(partitions)

#"***********************************************************************************************"
# Create List of TopicPartition Object for all the partitions present in a toic
tp = [TopicPartition(topic, partition) for partition in partitions]

# Get dictionary of latest message offset present in a topic partition; topic partition as key and lastest message offset as value
topic_partition_last_offset = consumer.end_offsets(tp)
print(topic_partition_last_offset)

# "***********************************************************************************************"

for i in tp:
    # Get offest of the last message processed by a consumer for a given Topic and its partition
    consumer_committed_offset=0 if consumer.committed(i) is None else consumer.committed(i)

    # From the dict of topic partition and its offset value, get the value for a given Topic and its partition
    last_offset_stored_by_broker_in_partition=topic_partition_last_offset[i]

    # Get lag
    lag=last_offset_stored_by_broker_in_partition-consumer_committed_offset
    print(f"Topic: {topic} - Partition: {i.partition} - Current Consumer Offset: {consumer_committed_offset} -  Last Offset: {last_offset_stored_by_broker_in_partition} - Lag : {lag}")
print('*'*100)