
##### Repartition Listener Example - Consumer 1

import json
import pyodbc  # Assuming pyodbc for SQL Server connection
from kafka import KafkaConsumer, TopicPartition, OffsetAndMetadata, ConsumerRebalanceListener 

# SQL Server connection setup
connection_str = "DRIVER={SQL Server};SERVER=localhost;DATABASE=TRYIT;UID=js;PWD=js"

# Table Structure in SQL SEVER, Which will be used to store the Offset during partition assignement or revocation

# CREATE TABLE kafka_offsets (
#     topic NVARCHAR(255) NOT NULL,          -- Kafka topic name
#     partition_id INT NOT NULL,             -- Partition ID
#     offset BIGINT NOT NULL,                -- Offset position in the partition 
# );


""" Create Rebalance Listener Class
        1. on_partitions_revoked - 
            This function will be used whenever a partition is revoked from a consumer of a consumer group.
            Whenever a partition is revoked, consumer offset will be written to a DB table.
        2. on_partitions_assigned - 
            This function will be used whenever a partition is assigned to a consumer of a consumer group.
            Whenever a partition is assigned, consumer offset will be read from the DB table and consumer will use seek method to start processing from that message offset onwards in that partition.
        3. consumer.seek(TopicPartition class,offset) method - 
            This will be used to make consumer start consuming from the offset returned from DB Table.
            TopicPartition class is a combination of Topic and Partition Id.
        4. Table Structure in the DB - 
            Table will have 3 columns to store - topic_name, partition_id and offset.
        5. Note: Combination of Topic, Partition Id and Offset will be used to implement the rebalance listener
"""
class MyConsumerRebalanceListener(ConsumerRebalanceListener):
    def __init__(self, consumer):
        self.consumer = consumer

    def on_partitions_revoked(self, revoked_partitions):
        print("Partitions %s revoked" % revoked_partitions)
        print('*' * 50)
        self.store_offsets(revoked_partitions)

    def on_partitions_assigned(self, assigned_partitions):
        print("Partitions %s assigned" % assigned_partitions)
        print('*' * 50)
        self.read_offsets(assigned_partitions)

    def store_offsets(self, partitions):
        try:
            with pyodbc.connect(connection_str, autocommit=False) as conn:
                cursor = conn.cursor()
                for partition in partitions:
                    tp = TopicPartition(partition.topic, partition.partition)
                    committed_offset = self.consumer.committed(tp)

                    if committed_offset is not None:
                        print("Committed Offset Available for partition:", partition)
                        # print("Topic:", partition.topic, "Partition:", partition.partition, "Offset:", committed_offset)
                        
                        # Execute the MERGE statement
                        cursor.execute(
                            """MERGE INTO TRYIT.dbo.kafka_offsets AS target
                            USING (VALUES (?, ?, ?)) AS source (topic, partition_id, offset)
                            ON target.topic = source.topic AND target.partition_id = source.partition_id
                            WHEN MATCHED THEN UPDATE SET target.offset = source.offset
                            WHEN NOT MATCHED THEN INSERT (topic, partition_id, offset)
                            VALUES (source.topic, source.partition_id, source.offset);""",
                            tp.topic, tp.partition, committed_offset
                        )
                        # Commit transaction after each successful write
                        conn.commit()
                        print("Data is successfully written to DB Table")
                    else:
                        print("No Committed Offset Available for partition:", partition)
        except Exception as e:
            print(e)

    def read_offsets(self, partitions):
        try:
            with pyodbc.connect(connection_str) as conn:
                cursor = conn.cursor()
                for partition in partitions:
                    cursor.execute(
                        "SELECT offset FROM TRYIT.dbo.kafka_offsets WHERE topic = ? AND partition_id = ?",
                        partition.topic, partition.partition
                    )
                    row = cursor.fetchone()
                    if row:
                        offset = row[0]
                        tp = TopicPartition(partition.topic, partition.partition)
                        # self.consumer.assign([tp])
                        self.consumer.seek(tp, offset)
        except Exception as e:
            print(e)


# Initialize the consumer 
consumer = KafkaConsumer(
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    group_id='demo112215sgtrjwrykvjh',
    auto_offset_reset='earliest',
    enable_auto_commit=False
)

# Initilize listener
listener = MyConsumerRebalanceListener(consumer)

# Create topic (uncomment and run in command line if needed)
# kafka-topics --create --topic rebalancer-topic --bootstrap-server localhost:9092 --replication-factor 1 --partitions 2

topic_name = 'rebalancer-topic'
consumer.subscribe([topic_name], listener=listener)

# Processing messages and committing offsets
for message in consumer:
    print(message)
    print("The value is : {}".format(message.value))
    tp = TopicPartition(message.topic, message.partition)
    om = OffsetAndMetadata(message.offset + 1, message.timestamp)
    consumer.commit({tp: om})
