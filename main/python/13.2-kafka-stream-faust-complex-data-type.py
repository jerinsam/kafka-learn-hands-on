"""
Script Name : 13.2-kafka-stream-faust-complex-data-type.py

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
create complex data type using python class
"""
class Greetings(faust.Record, serializer = 'json'):
    fromUser : str
    toUser : str

"""
After starting zookeeper and kafka broker - 
1. create an input topic using below script.
    kafka-topics --bootstrap-server localhost:9092 --create --topic test-stream

2. create an output topic using below script.
    kafka-topics --bootstrap-server localhost:9092 --create --topic test-stream-output
"""
app = faust.App("stream-processing-new",broker = 'localhost:9092')

# Input Topic Initialization
topic_name = 'test-stream'
topic = app.topic(topic_name, value_type = Greetings)

# Output Topic Initialization
output_topic_name = 'test-stream-output'
output_topic = app.topic(output_topic_name, value_type = str, value_serializer='raw')

"""
Create a kafka console producer using following script and push data to the topic. 
    Script : kafka-console-producer --bootstrap-server localhost:9092 --topic test-stream
    Example Message : {"fromUser":"Jerin","toUser":"Neeraj"}

Below python code, will consume the messages received from the input topic and display the transformed messages and will further push to output topic.
"""
@app.agent(topic)
async def processor(stream):
    async for message in stream:
        # Read message from Input Topic and Transform the message
        transformedMessage = f"Greetings from {message.fromUser} to {message.toUser}"
        print(transformedMessage)

        """
        Transformed Message is published back to Output Topic
        Use below script to start a kafka console consumer to see Output topic messages which is published by Kafka Stream Transformation
            kafka-console-consumer --bootstrap-server localhost:9092  --topic test-stream-output
        """
        await output_topic.send(value=transformedMessage)