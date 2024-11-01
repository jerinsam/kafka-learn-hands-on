"""
Script Name : 13.6-kafka-stream-faust-table-windowing.py

install Faust using - pip install faust-streaming

To execute this python file, rename it to main.py and execute below script in command prompt. 
    faust -A main worker -l info 
"""

import faust # install using - pip install faust-streaming

"""
Define a class to accept JSON Messages
"""
class carSchema(faust.Record, serializer='json'):
    car_id: int
    car_name: str
    car_speed: int
    capture_time: int

"""
After starting zookeeper and kafka broker - 
1. create an input topic using below script.
    Script : kafka-topics --bootstrap-server localhost:9092 --create --topic tumbling-window-topic - partitions 1
"""
app = faust.App("tumbling-window-app_1221",broker = 'localhost:9092', topic_partitions = 1)

# Input Topic Initialization
topic_name = 'tumbling-window-topic'
topic = app.topic(topic_name, value_type = carSchema)

# Create a Table
output_table = app.Table("faust-table-tumbling",key_type = str , value_type = int, default= int).tumbling(1)

"""
Python Producer : 13.5-kafka-stream-producer-for-windowing.py
"""
@app.agent(topic)
async def processor(stream):
    async for message in stream:
        # Read messages and output Tunbling Window aggregate
        print(message)
        output_table['Total']+=message.car_speed
        print("Current total : ",output_table['Total'].value())
        