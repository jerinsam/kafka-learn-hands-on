## Learn kafka on Landoop or on Windows

###### Open landoop kafka docker bash in CMD and mount local dev folder to docker - use below command
###### Directories are generally mounted for consuming the files present in host system by docker.
###### If the below command does not work then, docker copy command can be exected to move files from host system to docker
    docker run --rm -it -v %cd%:/main --net=host landoop/fast-data-dev bash


###### Open docker bash in CMD without mounting any directory - use below command
    docker run --rm -it --net=host landoop/fast-data-dev bash


###### Create new topic
    kafka-topics --create --topic test-topic --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1


###### List kafka topic
    kafka-topics --bootstrap-server localhost:9092 --list


###### Console kafka producer - Starts console producer
    kafka-console-producer --bootstrap-server localhost:9092 --topic test-topic


###### Console kafka Consumer - Starts console consumer
    kafka-console-consumer --bootstrap-server localhost:9092 --topic test-topic --from-beginning


###### Create new topic with 3 partitions
    kafka-topics --create --topic test-topic --bootstrap-server localhost:9092 --replication-factor 1 --partitions 3


###### Console kafka Consumer - Configure consumer to get the messages from a specific partition
    kafka-console-consumer --bootstrap-server localhost:9092 --topic test-topic --partition 1


###### Console kafka Consumer - Configure consumer to get the messages from a specific Offset
    kafka-console-consumer --bootstrap-server localhost:9092 --topic test-topic --partition 1 --offset 1


###### Console kafka Consumer - configure consumer to get the messages from a specific Offset without configuring partition. Below code will throw error, while configuring offset, partition needs to be configured
    kafka-console-consumer --bootstrap-server localhost:9092 --topic test-topic --offset 1

###### Alter Topic to increase Partitions
    kafka-topics --alter --topic multi-replica-topic --bootstrap-server localhost:9092 --partitions 3

###### Check __consumer_offsets topic
    kafka-console-consumer --bootstrap-server localhost:9092 --topic __consumer_offsets --formatter "kafka.coordinator.group.GroupMetadataManager$OffsetsMessageFormatter" --from-beginning

###### Delete Topic
    https://stackoverflow.com/questions/33537950/how-can-i-delete-a-topic-in-apache-kafka 


## Spin-up Kafka Cluster with 3 Brokers and test it by creating Topics, Producers and Consumers (for this exercise,  windows version of kafka is used)


###### Start Zookeeper using below code - change path of zookeeper.properties 
    zookeeper-server-start D:\kafka\config\zookeeper.properties


###### Start kafka clsuter - multiple brokers 
    kafka-server-start D:\kafka\config\server0.properties
    kafka-server-start D:\kafka\config\server1.properties
    kafka-server-start D:\kafka\config\server2.properties


###### Test kafka by creating a topic
    kafka-topics --create --topic multi-broker-topic-topic --bootstrap-server localhost:9092,localhost:9093,localhost:9094 --replication-factor 1 --partitions 5


###### Create kafka console Producer
    kafka-console-producer --topic multi-broker-topic-topic --bootstrap-server localhost:9092,localhost:9093,localhost:9094


###### Create producer with key separator. Test Message - 1: Jerin, 2:ABCD etc...
    kafka-console-producer --bootstrap-server localhost:9092,localhost:9093,localhost:9094 --topic multi-broker-topic --property parse.key=true --property "key.separator=:"


###### Create kafka console consumer
    kafka-console-consumer --topic multi-broker-topic-topic --bootstrap-server localhost:9092,localhost:9093,localhost:9094


###### Create kafka console consumer to populate key and its values
    kafka-console-consumer --bootstrap-server localhost:9092,localhost:9093,localhost:9094 --topic multi-broker-topic --from-beginning --property print.key=true --property "key.separator=:"


###### Create a topic with muliple partitions and multiple replication factor
    kafka-topics --create --topic multi-replica-topic --bootstrap-server localhost:9092,localhost:9093,localhost:9094 --replication-factor 3 --partitions 7


###### Describe topic to check which partition is Leader
    kafka-topics --topic multi-replica-topic --bootstrap-server localhost:9092,localhost:9093,localhost:9094 --describe


###### Alter Topic to increase Partitions
    kafka-topics --alter --topic multi-replica-topic --bootstrap-server localhost:9092,localhost:9093,localhost:9094 --partitions 3

###### Check __consumer_offsets topic
    kafka-console-consumer --bootstrap-server localhost:9092,localhost:9093,localhost:9094 --topic __consumer_offsets --formatter "kafka.coordinator.group.GroupMetadataManager$OffsetsMessageFormatter" --from-beginning

###### Delete Topic
    https://stackoverflow.com/questions/33537950/how-can-i-delete-a-topic-in-apache-kafka 


### Consumer Group and Consumer Lag in the group

###### Console Kafka Consumer assignment to a consumer group
    kafka-console-consumer --bootstrap-server localhost:9092 --topic consumer-group-topic --from-beginning --group consumer-group-abc


###### Check consumer lag in a consumer group
    kafka-consumer-groups --bootstrap-server localhost:9092 --group demo-consumer-group --describe

### Kafka Log Directory file Inspection

###### Inspect log file
    kafka-run-class kafka.tools.DumpLogSegments --files D:\kafka\__manual-logs__\server-logs\index-file-topic-0/00000000000000000000.log --deep-iteration --print-data-log 

###### Inspect index file
    kafka-run-class kafka.tools.DumpLogSegments --files D:\kafka\__manual-logs__\server-logs\index-file-topic-0/00000000000000000000.index --deep-iteration --print-data-log 

###### Inspect timeindex file
    kafka-run-class kafka.tools.DumpLogSegments --files D:\kafka\__manual-logs__\server-logs\index-file-topic-0/00000000000000000000.timeindex --deep-iteration --print-data-log 

### Log Compaction
###### Create Kafka Topic with Log Compaction
    kafka-topics --create --topic log-compaction-topic --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --config cleanup.policy=compact --config min.cleanable.dirty.ratio=0.001 --config segment.ms=5000

###### Start the Producer – enable Key Value config 
    kafka-console-producer --topic log-compaction-topic --bootstrap-server localhost:9092 --property parse.key=true --property key.separator=, 

###### Start the Consumer – enable Key Value config
    kafka-console-consumer --topic log-compaction-topic --bootstrap-server localhost:9092 --from-beginning --property print.key=true --property key.separator=,

### Start Kafka Connect Server
###### kafka connect standalone server can be started using connect-standalone executable, with 2 parameters. 1. details of the worker i.e. the server details and 2. details of the configured connector
    connect-standalone D:\kafka\config\test-connect-worker.properties D:\kafka\config\test-connect-connector.properties


### Confluent REST Proxy
###### For this exercise- 
###### - Kafka Broker used for this exercise, is installed locally in Windows.
###### - Docker container of Confluent REST Proxy is used, which needs to be configured to add Kafka Broker listeners. 
###### - NOTE: Docker container configuration needs advertise listener to talk to Kafka Broker, while doing the configuration lots of error occurred which is documented in Appendix section of the Documentation.

###### Check List of Topics using REST API
    http://localhost:8082/topics

###### Send Message to Topic – Use POST Method
    http://localhost:8082/topics/test-rest-proxy

    HEADER – 
    Content-Type : application/vnd.kafka.json.v2+json

    BODY – 
    {"records":[{"value":{"name": "testUser"}}]}

###### Send Multiple Messages to Topic – Use POST Method – Messages is sent in Key Value pairs in records attribute of JSON
    http://localhost:8082/topics/test-rest-proxy

    HEADER – 
    Content-Type : application/vnd.kafka.json.v2+json

    BODY – 
    {
    "records": [
        {
        "key": "3",
        "value": {
            "id": "3",
            "customer_code": "3",
            "telephone": "888582154",
            "email": "supplier3@test.com",
            "language": "EN"        
        }
        },
    {
        "key": "2",
        "value": {
            "id": "2",
            "customer_code": "2",
            "telephone": "788682158",
            "email": "supplier2@test.com",
            "language": "EN"        
        }
        }
    ]
    }

