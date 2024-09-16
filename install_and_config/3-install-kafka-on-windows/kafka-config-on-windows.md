### Kafka on Windows (Standalone)

###### - Download binary files of kafka from Apache Kafka site
- https://kafka.apache.org/downloads

###### - Unzip the downloaded file and place it at a location

###### - Go to /bin/windows folder and copy the path and add it to the environmental variable

###### - Create 2 folders for zookeeper logs (zookeeper-logs) and server logs (server-logs)

###### - Add the location of zookeeper-logs folder (created in above step) in dataDir config propery present in zookeeper.properties file at config folder. 

###### - Add the location of server-logs folder (created in above step) in log.dirs config propery present in server.properties file at config folder. 

###### - Start Zookeeper using below code - change path of zookeeper.properties
    zookeeper-server-start D:\kafka\config\zookeeper.properties

###### - Start Kafka Server using below code - change path of server.properties
    kafka-server-start D:\kafka\config\server.properties

###### - Test kafka by creating a topic
    kafka-topics --create --topic test-topic --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1

###### - Create kafka console Producer
    kafka-console-producer --topic test-topic --bootstrap-server localhost:9092

###### - Create kafka console consumer
    kafka-console-consumer --topic test-topic --bootstrap-server localhost:9092



### Kafka on Windows (Kafka Cluster with 3 Brokers)

###### - Download binary files of kafka from Apache Kafka site
- https://kafka.apache.org/downloads

###### - Unzip the downloaded file and place it at a location

###### - Go to /bin/windows folder and copy the path and add it to the environmental variable

###### - Create 1 folders for zookeeper logs (zookeeper-logs) and 3 folders for server logs (server0-logs, server1-logs, server2-logs) 

###### - Create 3 copies of server.properties file from config folder and rename it to "server0.properties", "server1.properties", "server2.properties"

###### - In each server{0,1,2}.properties file, change the following property - 
    Server/ Broker 1 :
        - broker.id=0 # Broker Id should be unique for each broker
        - listeners=PLAINTEXT://localhost:9092 # Listener should be unique for each broker 
        - log.dirs=D:\kafka\__manual-logs__\server0-logs # Add the location of server0-logs folder (created in above step) in log.dirs config propery

    Server/ Broker 2 :
        - broker.id=1 # Broker Id should be unique for each broker
        - listeners=PLAINTEXT://localhost:9093 # Listener should be unique for each broker 
        - log.dirs=D:\kafka\__manual-logs__\server1-logs # Add the location of server0-logs folder (created in above step) in log.dirs config propery

    Server/ Broker 3 :
        - broker.id=1 # Broker Id should be unique for each broker
        - listeners=PLAINTEXT://localhost:9094 # Listener should be unique for each broker 
        - log.dirs=D:\kafka\__manual-logs__\server2-logs # Add the location of server0-logs folder (created in above step) in log.dirs config propery

###### - In consumer.properties and producer.properties file, change the following property -
    bootstrap.servers=localhost:9092,localhost:9093,localhost:9094

###### - Start Zookeeper using below code - change path of zookeeper.properties
    zookeeper-server-start D:\kafka\config\zookeeper.properties

###### - Start Kafka Server for all 3 brokers using below code - change path of server.properties
    kafka-server-start D:\kafka\config\server0.properties
    kafka-server-start D:\kafka\config\server1.properties
    kafka-server-start D:\kafka\config\server2.properties

###### - Check running Broker Ids
    zookeeper-shell localhost:2181 ls /brokers/ids

###### - Test kafka by creating a topic
    kafka-topics --create --topic test-cluster-topic --bootstrap-server localhost:9092,localhost:9093,localhost:9094 --replication-factor 1 --partitions 5

###### - Create kafka console Producer
    kafka-console-producer --topic test-cluster-topic --bootstrap-server localhost:9092,localhost:9093,localhost:9094

###### - Create kafka console consumer
    kafka-console-consumer --topic test-cluster-topic --bootstrap-server localhost:9092,localhost:9093,localhost:9094


### Errors while configuring

###### The input line is too long when starting kafka
__Resolution__ : Path of the kafka folder should be small.
__Refer link__ : https://stackoverflow.com/questions/48834927/the-input-line-is-too-long-when-starting-kafka

###### classpath is empty. please build the project first
__Resolution__ : Download binary version of Kafka
__Refer link__ : https://stackoverflow.com/questions/34081336/classpath-is-empty-please-build-the-project-first


### Other useful properties in server.properties file

###### - (OR) For assigning Rack Id, rack information needs to be set -
    
    In each server{0,1,2}.properties files, add an additional property "broker.rack" - 

        Server/ Broker 1 :
            - broker.rack=0 # rack id 0 is assigned to broker 1 

        Server/ Broker 2 :
            - broker.id=1 # rack id 1 is assigned to broker 2  

        Server/ Broker 3 :
            - broker.id=0 # rack id 0 is assigned to broker 3 

###### - (OR) For Log Segment file management, Log segment file size needs to be set -
    
    In each server{0,1,2}.properties files, update an additional property "log.retention.check.interval.ms" - 
    
        Server/ Broker 1 :
            - log.retention.check.interval.ms=1000 # After 1000 bytes, new log segment (file) will be created 

        Server/ Broker 2 :
            - log.retention.check.interval.ms=1000 # After 1000 bytes, new log segment (file) will be created

        Server/ Broker 3 :
            - log.retention.check.interval.ms=1000 # After 1000 bytes, new log segment (file) will be created


