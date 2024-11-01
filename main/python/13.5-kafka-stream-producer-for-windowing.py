
# Producer code for Tumbling Window using Faust Table

from time import sleep
from json import dumps
from kafka import KafkaProducer
import random
import time

"""
After starting zookeeper and kafka broker - 
1. create an input topic using below script.
    Script : kafka-topics --bootstrap-server localhost:9092 --create --topic tumbling-window-topic - partitions 1
"""

topic_name='tumbling-window-topic'

def custom_partitioner(key, all_partitions, available):
    return int(key.decode('UTF-8'))%len(all_partitions)


producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'),
                         partitioner=custom_partitioner)

list_car=[{"car_id": 1, "car_name": "Honda", "car_speed": 5},
{"car_id": 2, "car_name": "Tesla", "car_speed": 3},
{"car_id": 3, "car_name": "Volvo", "car_speed": 8},
{"car_id": 4, "car_name": "Honda", "car_speed": 9},
{"car_id": 5, "car_name": "Tesla", "car_speed": 2},
{"car_id": 6, "car_name": "Volvo", "car_speed": 8},
{"car_id": 7, "car_name": "Honda", "car_speed": 5},
{"car_id": 8, "car_name": "Tesla", "car_speed": 7},
{"car_id": 9, "car_name": "Volvo", "car_speed": 1},
{"car_id": 10, "car_name": "Volvo", "car_speed": 5},
{"car_id": 11, "car_name": "Volvo", "car_speed": 2},
{"car_id": 12, "car_name": "Volvo", "car_speed": 3},
{"car_id": 13, "car_name": "Volvo", "car_speed": 6},
{"car_id": 14, "car_name": "Volvo", "car_speed": 5},
{"car_id": 15, "car_name": "Volvo", "car_speed": 3},
{"car_id": 16, "car_name": "Volvo", "car_speed": 1},
{"car_id": 17, "car_name": "Volvo", "car_speed": 8},
{"car_id": 18, "car_name": "Volvo", "car_speed": 9}]

###### Below code is used to generate time in above dictionary data, controlled at 1 second

for e in range(0,len(list_car)):
    if e in (2,5,8,12,14,17):
        list_car[e]['capture_time'] = int(time.time())
        print("Inserting the data : ",list_car[e])
        producer.send(topic_name, key=str(e).encode(), value=(list_car[e]))
        sleep(1)
    else:
        list_car[e]['capture_time'] = int(time.time())
        print("Inserting the data : ", list_car[e])
        producer.send(topic_name, key=str(e).encode(), value=(list_car[e]))