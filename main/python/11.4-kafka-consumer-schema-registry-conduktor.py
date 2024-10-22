
####### Python Script : Using Schema Registry and Kafka Broker from Conduktor's Kafka Docker ##########

# pip install confluent_kafka

#### Get the details of the port from Docker Compose yaml file of Conduktor ####
# Kafka Broker Bootstrap Server External : localhost:19092
# Schema Registry External URL : http://localhost:18081


from confluent_kafka.schema_registry import SchemaRegistryClient, Schema
from confluent_kafka.schema_registry.avro import AvroDeserializer 
from confluent_kafka.serialization import SerializationContext, MessageField
from time import sleep
from json import dumps
from kafka import KafkaConsumer  
from kafka import TopicPartition , OffsetAndMetadata

# create variables
topic_name = 'schema_registry-test'
schema_registry_url = 'http://localhost:18081' 
subject_name = topic_name+'-value'

# create a schema registry client
schema_registry_config = {"url": schema_registry_url}
schema_registry_client = SchemaRegistryClient(schema_registry_config)

# get schema from schema registry, the return type is of type RegisteredSchema which is a class
registered_schema = schema_registry_client.get_latest_version(subject_name) 


# another way to get the latest version of schema from a subject
# schema_version = schema_registry_client.get_versions(subject_name)
# schema = schema_registry_client.get_version(subject_name, schema_version[-1]) 

 
# Create an Avro deserializer object using AvroDeserializer class
avro_deserializer = AvroDeserializer(schema_registry_client, registered_schema.schema)
 

#create serialization context : provides additional context to the serializer about the data it’s serializing.
sc = SerializationContext(topic_name, MessageField.VALUE)

# create consumer 
# value deserialization can be done while initializing the consumer or can also be done while processing the message

consumer = KafkaConsumer( topic_name, bootstrap_servers=['localhost:19092'] ,  
group_id='testingschemaregistry', auto_offset_reset='earliest', enable_auto_commit =False,
value_deserializer = lambda x: avro_deserializer(x, sc) )


'''
1. Whenever a message is received/ polled, Schema Id which was transmitted by Producer will be used to fetch the Schema from Schema Registry.
2. Fetched Schema will be used to deserialize the message
'''

for message in consumer:
    print(message)
    
    # value deserialization can be done while initializing the consumer or can also be done while processing the message as shown below
    # print("The value is : {}".format(avro_deserializer(message.value, sc))
    
    print("The value is : {}".format(message.value))
    print("The key is : {}".format(message.key)) 
    tp = TopicPartition(message.topic,message.partition)
    om = OffsetAndMetadata(message.offset+1, message.timestamp)
    consumer.commit({tp:om})
    print('*' * 100)


