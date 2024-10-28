### Kafka Connect Standalone Server Configuration
In this exercise, SQL SERVER Source connector will be used

##### STEP 1 - Download the SQL SERVER Source connector from Confluent Connector hub
    1.1. Download the SQL SERVER Source connector from Confluent Connector hub 
    https://www.confluent.io/hub/#  
    1.2. Extarct the downloaded file and save it at /lib/ folder present in the Kafka installed directory

##### STEP 2 - Enable CDC on a SQL Server Table
    1.1. Enable CDC on a SQL Server Table, This table details will be mentioned in the connector configuration 
    1.2. Details on enabling CDC can be found in file "sql-query-change-data-capture-config.sql"

##### STEP 3 - Prepare 2 files that are required to start the kafka connect standalone server
###### 1. Details of the worker i.e. server details (File Name - test-connect-worker.properties)
    1.1. Go to /config/ folder in the Kafka installed directory
    1.2. Copy and Paste /config/connect-standalone.properties and rename it to /config/test-connect-worker.properties
    1.3. Open /config/test-connect-worker.properties and change "plugin.path" to the /lib/ folder present in the Kafka installed directory
    1.4. In /config/test-connect-worker.properties file, change "offset.storage.file.filename" to a path which can be accessed or a path which can be resolved (i.e. correct path name or correctly formatted).
    1.5. Close and save the file
###### 2. Details of the connector with the configuration details (File Name - test-connect-connector.properties)
    1.1 Create a file called test-connect-connector.properties, which will contain all the configuration of the connector like DB name, port, CDC enabled table name, connector class etc.
    1.2. While providing the DB host ip address, run command ipconfig and get the latest ip address.
    1.3 While passing the values, make sure spaces does not exist at the end of the property values, else while starting the kafka connect standalone cluster, it will throw error.
    1.4 Close and save the file

##### STEP 4 - Start Kafka Standalone Server using below script
###### connect-standalone executable will be used to start the Kafka Standalone Server, above cerated files will be used as the parameter in this script
    connect-standalone D:\kafka\config\test-connect-worker.properties D:\kafka\config\test-connect-connector.properties


### Errors received during the configuration
###### 1. Due to leading spaces in the value section of the property "value.converter" & "database.hostname" of the properties files, following errors were occuring. 
    1. Failed to load class org.apache.kafka.connect.json.JsonConverter : org.apache.kafka.connect.json.JsonConverter
    2. The 'database.hostname' value is invalid: 10.10.13.34  has invalid format (only the underscore, hyphen, dot and alphanumeric characters are allowed)

###### 2. Make sure topic mentioned in the connector properties exist or already cerated before starting the server. 

###### 3. Make sure CDC enabled table details are provided in the connector configuration i.e. in File Name - test-connect-connector.properties