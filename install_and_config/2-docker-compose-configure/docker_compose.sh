

###### In this tutorial, Landoop Kafka container will be used #######
# url : https://hub.docker.com/r/landoop/fast-data-dev 
# details of the environment mentioned in docker compose yaml file can be found in above link

###### Elasticsearch container #########
# url : https://hub.docker.com/_/elasticsearch

# Download Docker Desktop for Windows and run it
# Execute the below command to pull and configure all the images defined in the docker-compose.yaml file
# this needs to be executed in the same folder where docker-compose.yaml file exists

docker compose up -d # to start all the services mentioned in the docker compose yaml file

docker-compose start kafka-cluster # to start only 1 service from the docker compose yaml file

docker-compose stop # to stop all container services 

docker-compose stop kafka-cluster # to stop one container services 

#To connect to services in Docker, refer to the following ports. 
  
# Zookeeper - 2181:2181
# Landoop UI - 3030:3030
# REST Proxy, Schema Registry, Kafka Connect - 8081-8083:8081-8083
# JMX - 9581-9585:9581-9585
# Kafka Broker - 9092:9092
# Elasticsearch - 9200
 

##### open docker bash in CMD and map local dev folder to docker - use below command ######
# docker run --rm -it -v %cd%:/tutorial --net=host landoop/fast-data-dev:cp3.3.0 bash
