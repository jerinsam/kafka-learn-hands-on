"""
Script Name : 13.3-kafka-stream-faust-table.py

install Faust using - pip install faust-streaming

To execute this python file, rename it to main.py and execute below script in command prompt. 
    faust -A main worker -l info
"""

import faust # install using - pip install faust-streaming

"""
After starting zookeeper and kafka broker - 
1. create an input topic using below script.
    kafka-topics --bootstrap-server localhost:9092 --create --topic word-count-stream 
"""
app = faust.App("stream-processing-new",broker = 'localhost:9092', topic_partitions = 1)

# Input Topic Initialization
topic_name = 'word-count-stream'
topic = app.topic(topic_name, value_type = str, value_serializer='raw')

# Create a Table
output_table = app.Table("faust-test-table",key_type = str , value_type = int, partitions= 1 , default= int)

"""
Create a kafka console producer using following script and push data to the topic. 
    kafka-console-producer --bootstrap-server localhost:9092 --topic word-count-stream

Below python code, will consume the messages received from the input topic and add the records to a Table.
"""
@app.agent(topic)
async def processor(stream):
    async for message in stream:
        # Read message from Input Topic and Transform the message
        
        listOfWords = message.split()        
        for i in listOfWords:
            output_table[i]+=1

        print(output_table.as_ansitable(title = "TestTable"))