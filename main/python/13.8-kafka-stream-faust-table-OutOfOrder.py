"""
Script Name : 13.8-kafka-stream-faust-table-OutOfOrder.py

install Faust using - pip install faust-streaming

To execute this python file, rename it to main.py and execute below script in command prompt. 
    faust -A main worker -l info 
"""

import faust # install using - pip install faust-streaming
from datetime import datetime, timedelta
from time import time

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
    Script : kafka-topics --bootstrap-server localhost:9092 --create --topic out-of-order-tumbling - partitions 1
"""

# Variable for Clean-up interval
CLEANUP_INTERVAL = 60

# Variable for Window Expirt
WINDOW_EXPIRES = 60

app = faust.App("tumbling-OutOfOrder-App",broker = 'localhost:9092', topic_partitions = 1)

# Remove message from memory after value in seconds mentioned in CLEANUP_INTERVAL variable
app.conf.table_cleanup_interval = CLEANUP_INTERVAL


# Input Topic Initialization
topic_name = 'out-of-order-tumbling'
topic = app.topic(topic_name, value_type = carSchema)

# This summarization function will be executed after the window closes i.e. after window expiry
def window_processor(key, events):

    ''' 
        key and events are the columns of Faust Table
    ''' 
    print("############################### Window Processor Started #####################################")
    print("-------------------------------- Key--------------------------------")
    print(key)
    print("-------------------------------- Events--------------------------------")
    print(events)

    # Example of Key : ('events', (1730456943.0, 1730456943.9)) 
    start_time = key[1][0] 
    end_time = key[1][1]

    # Example of events column: 
    #   [
    #       <carSchema: car_id=1, car_name='Honda', car_speed=5, capture_time=1730456943>, 
    #       <carSchema: car_id=2, car_name='Tesla', car_speed=3, capture_time=1730456943>, 
    #       <carSchema: car_id=3, car_name='Volvo', car_speed=8, capture_time=1730456943>,
    #       <carSchema: car_id=2000, car_name='Alto', car_speed=300, capture_time=1730456943>
    #   ]

    values = [event.car_speed for event in events]
    total_value = sum(values)

    print(
    "Total Car Speed between {} & {} is {}".format(start_time, end_time, total_value)
    )
    print("############################### Window Processor Completed #####################################")


# Create a Table
output_table = app.Table("OOO-Late-Arriving", default=list, on_window_close=window_processor). \
    tumbling(1, expires=timedelta(seconds=WINDOW_EXPIRES)) \
    .relative_to_field(carSchema.capture_time)

"""
Python Producer : 13.7-kafka-stream-producer-for-OutOfOrder.py
"""
@app.agent(topic)
async def processor(stream):
    async for message in stream:
        # Read messages/out of order messages and output Tunbling Window aggregate

        """ 
            Consolidate all the message values in the Table memory till window expires. 
            List of messages will be saved in a column of Faust Table called events.
        """
        
        # Read list of messages already saved in the Faust table column "events": Initially it will be blank i.e. will be blank at the start of a new window
        value_list = output_table['events'].value() 
       
        # Save the new message in the list
        value_list.append(message)

        # Update table column "events" with new message list
        output_table['events'] = value_list

        print(output_table['events'].value())
        