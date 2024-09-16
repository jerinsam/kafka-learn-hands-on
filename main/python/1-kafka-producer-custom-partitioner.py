# Start Zookeeper and Broker
# Create Topic
# Code for customized partitioner

from time import sleep
from json import dumps
from kafka import KafkaProducer


def custom_partitioner(key, all_partitions, available):
    """
    Customer Kafka partitioner to get the partition corresponding to key
    :param key: partitioning key
    :param all_partitions: list of all partitions sorted by partition ID
    :param available: list of available partitions in no particular order
    :return: one of the values from all_partitions or available
    """
    print("The key is  : {}".format(key))
    print("All partitions : {}".format(all_partitions))
    print("After decoding of the key : {}".format(key.decode('UTF-8')))
    return int(key.decode('UTF-8'))%len(all_partitions)


producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    partitioner=custom_partitioner, 
    key_serializer=str.encode,
    value_serializer=lambda x: dumps(x).encode('utf-8')
)
topic_name='test-custom-partitioner'

producer.send(topic_name, key='3', value={'Name': 'Jerin'})
producer.send(topic_name, key='2', value={'Name': 'Priti'})
producer.send(topic_name, key='369', value={'Name': 'Ajit'})
producer.send(topic_name, key='301', value={'Name': 'Ashu'})

'''
If a producer is configured with custom partitioner and while sending a message if partition parameter is used
then the partition mentioned will supersede the custom partitioner
'''
producer.send(topic_name, key='3', value={'Name': 'HeyParttionBypass'} , partition=2)

producer.close()
