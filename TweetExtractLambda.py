from __future__ import print_function
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from textwrap import TextWrapper
import json
import time
import boto3
import requests

#Twiiter credentials
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

#Initiate sqs queue
sqs = boto3.client(
    'sqs',
    aws_access_key_id = '',
    aws_secret_access_key = '',
    region_name = 'us-west-2'
)

def lambda_handler(event, context):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    twitter_stream = Stream(auth, TweetListener())
    twitter_stream.filter(languages=["en"],track=['trump','messi','MissUniverse','iphone x','worldcup','#arsmun','manchester','#arsenal','photo','madrid','band'])
    print ("Adding data to queue")
    
class TweetListener(StreamListener):
    def on_data(self, data):
        try:
            status_wrapper = TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')
            twitter_data = json.loads(data)
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
                    print(tweet)
                    sqs.send_message(QueueUrl = 'https://sqs.us-west-2.amazonaws.com/435250124029/Queue1', MessageBody=json.dumps(tweet))  #Adding data to Queue1                 
                    return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True
