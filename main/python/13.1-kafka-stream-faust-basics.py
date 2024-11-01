"""
Script Name : 13.1-kafka-stream-faust-basics.py

install Faust using - pip install faust-streaming

To execute this python file, rename it to main.py and execute below script in command prompt. 
    faust -A main worker -l info
    faust -A main worker -l info --web-port=6067 

Executing the same python code twice using different ports (as mentioned above, port 6067) enable parallelism in Faust. 
Example - 
    1. If a topic has 2 partitions and executing the Faust code twice will assign 1 partition each to both the running Faust instances.
    2. If there's only 1 Faust instance running then both the partitions will be assigned to that 1 Faust instance.
"""

import faust # install using - pip install faust-streaming

"""
After starting zookeeper and kafka broker - 
1. create an input topic using below script.
    kafka-topics --bootstrap-server localhost:9092 --create --topic test-stream --partitions 2
"""
app = faust.App("stream-processing",broker = 'localhost:9092')

topic_name = 'test-stream'
topic = app.topic(topic_name, value_type = str , value_serializer = 'raw')

"""
Create a kafka console producer using following script and push data to the topic. 
    1. Normal Kafka Console Producer
        kafka-console-producer --bootstrap-server localhost:9092 --topic test-stream

    2. Console Producer with Key and Value - To Test Parallelism in Faust
        kafka-console-producer --bootstrap-server localhost:9092 --topic test-stream-2 --property parse.key=true --property "key.separator=:"

Below python code, will consume the messages received from the input topic and display the transformed messages.
"""
@app.agent(topic)
async def processor(stream):
    async for message in stream:
        print(f"Received message : {message}")