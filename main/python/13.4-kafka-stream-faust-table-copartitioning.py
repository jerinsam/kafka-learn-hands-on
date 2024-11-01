"""
Script Name : 13.4-kafka-stream-faust-table-copartitioning.py

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
Define a class to accept JSON Messages
"""
class countryUI(faust.Record, serializer = 'json'):
    UID : int
    Country : str

"""
After starting zookeeper and kafka broker - 
1. create an input topic using below script.
    Script : kafka-topics --bootstrap-server localhost:9092 --create --topic copartition-table - partitions 3 
"""
app = faust.App("stream-processing-table-partition",broker = 'localhost:9092', topic_partitions = 3)

# Input Topic Initialization
topic_name = 'copartition-table'
topic = app.topic(topic_name, value_type = countryUI)

# Create a Table
output_table = app.Table("faust-table-copartition",key_type = str , value_type = int, default= int)

"""
Create a kafka console producer using following script and push data to the topic. 
    Script : kafka-console-producer --bootstrap-server localhost:9092 --topic copartition-table
    Example Messages : 
        1. {"UID":1,"Country":"India"} 
        2. {"UID":2,"Country":"US"}
        3. {"UID":3,"Country":"UK"}
        4. {"UID":4,"Country":"India"} 
        5. {"UID":5,"Country":"US"}
        6. {"UID":6,"Country":"UK"}
        7. {"UID":7,"Country":"India"}
        8. {"UID":8,"Country":"US"}
        9. {"UID":9,"Country":"UK"}

Below python code, will consume the messages received from the input topic and add the records to a Table.
"""
@app.agent(topic)
async def processor(stream):
    async for message in stream.group_by(countryUI.Country):
        # Read message from Input Topic and Transform the message
        output_table[message.Country]+=1
        print(output_table.as_ansitable(title = "TestTable"))