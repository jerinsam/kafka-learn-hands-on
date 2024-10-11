
####### Python Script : Using AWS Glue as Schema Registry and Kafka Broker from Conduktor's Kafka Docker ##########


#pip3 install boto3 -t.
#pip3 install aws-glue-schema-registry --upgrade --use-pep517 -t .
#pip install kafka-python -t .

import boto3
from aws_schema_registry import SchemaRegistryClient
from kafka import TopicPartition , OffsetAndMetadata
from aws_schema_registry.adapter.kafka import KafkaDeserializer
from kafka import KafkaConsumer

# Add AWS Access Key and Secret
session = boto3.Session(aws_access_key_id='{}', aws_secret_access_key='{}')

# Create Glue client
glue_client = session.client('glue', region_name='us-east-1')


# Create the schema registry client, which is a façade around the boto3 glue client
client = SchemaRegistryClient(glue_client,
                              registry_name='my-registry')

# Create the deserializer
deserializer = KafkaDeserializer(client)

# Add bootstrap server, consumer group id
consumer = KafkaConsumer ('topic2',bootstrap_servers = ['{}'],
value_deserializer=deserializer, group_id='{}',
auto_offset_reset='earliest', enable_auto_commit =False
)

'''
1. Whenever a message is received/ polled, Schema Id which was transmitted by Producer will be used to fetch the Schema from Schema Registry.
2. Fetched Schema will be used to deserialize the message
'''
for message in consumer:
    print(message)
    print("The value is : {}".format(message.value))
    print("The key is : {}".format(message.key))
    print("The topic is : {}".format(message.topic))
    print("The partition is : {}".format(message.partition))
    print("The offset is : {}".format(message.offset))
    print("The timestamp is : {}".format(message.timestamp))
    tp=TopicPartition(message.topic,message.partition)
    om = OffsetAndMetadata(message.offset+1, message.timestamp)
    consumer.commit({tp:om})
    print('*' * 100)