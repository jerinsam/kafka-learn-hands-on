
####### Not Tested as AWS S3 credentials are required ##########

import faust
from faust import Record
import logging
from faust_large_message_serializer import LargeMessageSerializer, LargeMessageSerializerConfig
from faust.serializers import codecs
import random
import time
 

# s3_json data schema

# message schema class
class UserModel(Record, serializer="s3_json"):
    comment: str

# configure large message serializer
config = LargeMessageSerializerConfig(base_path="s3://irisseta/",
                                      max_size=100, # set max size of messages to be handled by Kafka, its 100 bytes in this example
                                      large_message_s3_region="us-east-1",
                                      large_message_s3_access_key="",
                                      large_message_s3_secret_key="")

topic_name = "users_s3"

s3_backed_serializer = LargeMessageSerializer(topic_name, config, is_key=False)
json_serializer = codecs.get_codec("json")

# Here we use json as the first serializer and
# then we can upload everything to the S3 bucket to handle messages exceeding the configured maximum message size.

s3_json_serializer = json_serializer | s3_backed_serializer


logger = logging.getLogger(__name__)

# register serializer - config
codecs.register("s3_json", s3_json_serializer)

# config app 
app = faust.App("app_id", broker="kafka://localhost:9092")
users_topic = app.topic(topic_name, value_type=UserModel)


# receive data 
@app.agent(users_topic)
async def users(users):
    async for user in users:
        print("The received event is : ",user)