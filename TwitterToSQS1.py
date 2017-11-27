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


#Twiiter credentials
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
    region_name = ''
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
                    print(count)
                    print(tweet)
                    sqs.send_message(QueueUrl = '', MessageBody=json.dumps(tweet))  #Adding data to Queue1                 
                    return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True

if __name__ == '__main__':
    twitter_stream = Stream(auth, TweetListener())
    twitter_stream.filter(languages=["en"],track=['trump','miss universe','messi','MissUniverse','bush','thanksgiving','iphone x','memory','death','nba','worldcup','birthday','photo','stranger things','election'])
