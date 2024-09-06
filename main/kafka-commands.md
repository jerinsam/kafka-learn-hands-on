### Learn kafka on Landoop or on Windows

###### Open landoop kafka docker bash in CMD and mount local dev folder to docker - use below command
###### Directories are generally mounted for consuming the files present in host system by docker.
###### If the below command does not work then, docker copy command can be exected to move files from host system to docker
        docker run --rm -it -v %cd%:/main --net=host landoop/fast-data-dev bash


###### open docker bash in CMD without mounting any directory - use below command
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



### Spin-up Kafka Cluster with 3 Brokers and test it by creating Topics, Producers and Consumers (for this exercise,  windows version of kafka is used)


###### - Start Zookeeper using below code - change path of zookeeper.properties 
    zookeeper-server-start D:\kafka\config\zookeeper.properties


###### Start kafka clsuter - multiple brokers 
        kafka-server-start D:\kafka\config\server0.properties
        kafka-server-start D:\kafka\config\server1.properties
        kafka-server-start D:\kafka\config\server2.properties


###### - Test kafka by creating a topic
    kafka-topics --create --topic multi-broker-topic-topic --bootstrap-server localhost:9092,localhost:9093,localhost:9094 --replication-factor 1 --partitions 5


###### - Create kafka console Producer
    kafka-console-producer --topic multi-broker-topic-topic --bootstrap-server localhost:9092,localhost:9093,localhost:9094


###### - Create producer with key separator. Test Message - 1: Jerin, 2:ABCD etc...
    kafka-console-producer --bootstrap-server localhost:9092,localhost:9093,localhost:9094 --topic multi-broker-topic --property parse.key=true --property "key.separator=:"


###### - Create kafka console consumer
    kafka-console-consumer --topic multi-broker-topic-topic --bootstrap-server localhost:9092,localhost:9093,localhost:9094


###### - Create kafka console consumer to populate key and its values
    kafka-console-consumer --bootstrap-server localhost:9092,localhost:9093,localhost:9094 --topic multi-broker-topic --from-beginning --property print.key=true --property "key.separator=:"


###### - Create a topic with muliple partitions and multiple replication factor
    kafka-topics --create --topic multi-replica-topic --bootstrap-server localhost:9092,localhost:9093,localhost:9094 --replication-factor 3 --partitions 7

###### - Describe topic to check which partition is Leader
    kafka-topics --topic multi-replica-topic --bootstrap-server localhost:9092,localhost:9093,localhost:9094 --describe

