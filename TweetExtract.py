import json
import tweepy
import boto3
from requests_aws4auth import AWS4Auth
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from boto.sqs.message import Message
from textwrap import TextWrapper
import requests
from elasticsearch import Elasticsearch, RequestsHttpConnection

consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

#Authorizing the twitter acount
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)
print("Twitter Authorization Successful!")
#Initiate sqs queue
sqs = boto3.client(
    'sqs',
    aws_access_key_id = '',
    aws_secret_access_key = '',
    region_name = 'us-west-2'
)

count = 0
print ("Adding data to queue")
class TweetListener(StreamListener):  
    def on_data(self, data):
        try:
            status_wrapper = TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')
            twitter_data = json.loads(data)
            m = Message()
            if ('coordinates' in twitter_data.keys()):
                if (twitter_data['coordinates'] is not None):
                    tweet = {
                        'id': twitter_data['id'],
                        'time': twitter_data['timestamp_ms'],
                        'text': twitter_data['text'].lower().encode('ascii', 'ignore').decode('ascii'),
                        'coordinates': twitter_data['coordinates'],
                        'place': twitter_data['place'],
                        'handle': twitter_data['user']['screen_name'],
                        'sentiment': ""
                    }

                    global count
                    count += 1
                    print (count)
                    sqs.send_message(QueueUrl = 'https://sqs.us-west-2.amazonaws.com/435250124029/Tweets', MessageBody=json.dumps(tweet))                   
                    return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


twitter_stream = Stream(auth, TweetListener())
try:
    twitter_stream.filter(languages=["en"],track=['trump','nba','photo','memories','party','birthday','fun','newyork'], locations = [-180, -90, 180, 90])
except (KeyError, TypeError):
    pass
