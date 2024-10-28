###### Go to Confluent Github page and Download Docker Compose File #######
# url : https://github.com/confluentinc/cp-all-in-one/tree/7.5.0-post/cp-all-in-one
# Folder : cp-all-in-one

# Download Docker Desktop for Windows and run it
# Download Docker Compose yaml file from the above mentioned github page and modify it by keeping only rest-proxy section 
# Refer docker-compose file in this folder for the reference.
"""
Important points while setting up REST Proxy:
•	For REST Proxy to communicate with the Kafka Broker, Kafka Broker's advertised.listener should be added in Rest Proxy's config file.
•	Since Docker container is used, therefore to add Kafka Broker's advertised.listener,  use container's environmental variable "KAFKA_REST_BOOTSTRAP_SERVERS"
•	REST PROXY Container's environmental variable "KAFKA_REST_BOOTSTRAP_SERVERS" should be the advertised.listener present in kafka broker's server.properties file
•	While adding host name to advertised.listener in kafka broker's server.properties file, make sure it should be Virtual Box IP which starts with 192.X.X.X:9092 
•	While in Production, Setup LISTENERS and ADVERTISED LISTENERS for REST PROXY as well
"""
# Execute the below command to pull and configure all the images defined in the docker-compose.yaml file
# this needs to be executed in the same folder where docker-compose.yaml file exists

docker compose up -d

# To stop Container Services 

docker-compose stop
 