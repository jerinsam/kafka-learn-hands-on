

###### In this tutorial, Conduktor UI with Redpanda Kafka container will be used #######
# url : https://docs.conduktor.io/platform/get-started/installation/get-started/docker/#step-1-launch-conduktor
# docker compose url : https://raw.githubusercontent.com/conduktor/conduktor-platform/main/quick-start.yml
# details of the environment mentioned in docker compose yaml file can be found in above link
 

# Download Docker Desktop for Windows and run it
# Execute the below command to pull and configure all the images defined in the docker-compose.yaml file
# this needs to be executed in the same folder where docker-compose.yaml file exists

#To connect to services in Docker, refer to the ports associated with services in docker-compose yaml file. 

docker compose up -d # to start all the services mentioned in the docker compose yaml file 

docker-compose stop # to stop all container services 
 
 