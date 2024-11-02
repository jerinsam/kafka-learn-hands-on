
####### Not Tested as AWS S3 credentials are required ##########

import faust
from faust import Record
import logging
from faust_large_message_serializer import LargeMessageSerializer, LargeMessageSerializerConfig
from faust.serializers import codecs
import random
import time

# data/ message to be sent
data_points=["Hello World","""Thank you so much for the explanation, I am currently building a project,
 I have never heard of object storage until this video, I always thought its just cloud database + cloud storage,
  this is such a neat idea !""","Nice presentation. It is very clearly summarized. Thanks a lot",
             """It seems like the object storage is used mainly for not-so-very-often used static unstructured data. Thus I'm a bit baffled by the recommendation to use it in a video-streaming service. Wouldn't SAN be a better solution if I wanted to design a YouTube-like site?
And, can we use buckets for a CDN-like solution?
Thanks!""","Bye","Check where message going","Hi There"]

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

# cerate serializers
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


# send data 
# Faust will automatically upload any message size exceeding 100 bytes to S3 bucket and send the URL to kafka

@app.timer(10.0)
async def send_users():
    data_user = {"comment":random.choice(data_points)}
    print(data_user)

    # convert message to an object of type schema class defined above
    user = UserModel(**data_user)
    await users_topic.send(value=user, value_serializer=s3_json_serializer)