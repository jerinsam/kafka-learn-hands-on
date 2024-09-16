 
#Asynchronous Send

from time import sleep
from json import dumps
from kafka import KafkaProducer

# Create topic using below script
# kafka-topics --create --topic test-message-sending-method --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1

topic_name='test-message-sending-method'
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))

# First parameter is the standard parameter for success
# The functions need standard parameter, i.e. 1st parameter should be the standard parameter "record_metadata"
# User can define other parameters

def on_send_success(record_metadata,message):
    print("""Successfully produced "{}" to topic {} and partition {} at offset {}""".format(message,record_metadata.topic,record_metadata.partition,record_metadata.offset))
    print()

# First parameter is the standard parameter for failure
# The functions need standard parameter, i.e. 1st parameter should be the standard parameter "exep"
# User can define other parameters

def on_send_error(excp,message):
    print('Failed to write the message "{}" , error : {}'.format(message,excp))

for e in range(100):
    data = {'number' : e}
    # add_callback method for success and add_errback for error
    # These methods take function as input
   
    record_metadata =producer.send(topic_name, value=data).add_callback(on_send_success,message=data).add_errback(on_send_error,message=data)
    print("Sent the message {} using send method".format(data))
    print()
    sleep(0.5)


producer.flush()
producer.close()