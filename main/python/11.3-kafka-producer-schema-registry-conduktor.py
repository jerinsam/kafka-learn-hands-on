
####### Python Script : Using Schema Registry and Kafka Broker from Conduktor's Kafka Docker ##########

# pip install confluent_kafka

#### Get the details of the port from Docker Compose yaml file of Conduktor ####
# Kafka Broker Bootstrap Server External : localhost:19092
# Schema Registry External URL : http://localhost:18081
# Topic "schema_registry-test" is created manually from Conduktor UI

 
from confluent_kafka.schema_registry import SchemaRegistryClient, Schema
from confluent_kafka.schema_registry.avro import AvroSerializer 
from confluent_kafka.serialization import SerializationContext, MessageField
from time import sleep
from json import dumps
from kafka import KafkaProducer  

# create variables
topic_name = 'schema_registry-test'
schema_registry_url = 'http://localhost:18081' 
subject_name = topic_name+'-value'
 
# read avro schema
with open("./schema-file/test-schema.avsc") as avro_schema_file:
        record_schema = avro_schema_file.read()
 
 
# create a schema registry client
schema_registry_config = {"url": schema_registry_url}
schema_registry_client = SchemaRegistryClient(schema_registry_config)

# register schema
schema = Schema(record_schema,"AVRO") #confluent requires schema of Type Schema
schema_id = schema_registry_client.register_schema(subject_name,schema)
# print(schema_id)

# Create an Avro serializer object using AvroSerializer class
avro_serializer = AvroSerializer(schema_registry_client, record_schema)
 

# Send message data along with schema
data = {
    'age':36,
    'name': 'Neeraj'
} 

# create producer 
producer = KafkaProducer(bootstrap_servers=['localhost:19092'])
 

#create serialization context : provides additional context to the serializer about the data it’s serializing.
sc = SerializationContext(topic_name, MessageField.VALUE)


'''
1. If Schema does not exist in Schema Registry or during first message transmission, then Schema will be registered.
2. Schema will be sent through value parameter as a tuple, format of value parameter should be (data, schema)
3. Schema will be validated against the schema in Schema Registry, after validation Schema Id will be attached to serialized message and will be transmitted to topic.
4. Serialization Context is used here in value parameter to provide additional context to the serializer about the data it’s serializing
'''

record_metadata =producer.send(topic_name, value=avro_serializer(data,sc)).get(timeout=10)
print(record_metadata.topic)
print(record_metadata.partition)
print(record_metadata.offset)

