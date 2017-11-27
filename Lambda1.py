import json
import time
import boto3
from monkeylearn import MonkeyLearn

from multiprocessing.dummy import Pool

sqs1 = boto3.client(
    'sqs',
    aws_access_key_id='',
    aws_secret_access_key='',
    region_name = ''
)
sqs = boto3.resource(
    'sqs',
    aws_access_key_id='',
    aws_secret_access_key='',
    region_name = ''
)

queue = sqs.get_queue_by_name(QueueName='Queue1')

sns = boto3.client(
    'sns',
    aws_access_key_id='',
    aws_secret_access_key='',
    region_name = ''
)
arn = 'arn:aws:sns:us-west-2:435250124029:TweetSNS'

module_id = 'cl_qkjxv9Ly'
ml = MonkeyLearn('')

def lambda_handler(event,context):
    while True:
        messages = queue.receive_messages(QueueUrl='https://sqs.us-west-2.amazonaws.com/435250124029/Queue1',AttributeNames=['SentTimestamp'],MaxNumberOfMessages=10,MessageAttributeNames=['All'],VisibilityTimeout=0,WaitTimeSeconds=0)
        #x = messages['Messages'][0]
        #receipt_handle = x['ReceiptHandle']
        #client.delete_message(QueueUrl=queue_url,ReceiptHandle=receipt_handle)
        
        for message in messages:
            tweet = json.loads(message.body)
            text = tweet["text"]
            print(text)
            print("Received event: " + json.dumps(event, indent=2))
            text_list = [ text ]
            lat = str(tweet["coordinates"]["coordinates"][1])
            lon = str(tweet["coordinates"]["coordinates"][0])
            place = tweet["place"]["country"]
            
            
    
            res = ml.classifiers.classify(module_id, text_list, sandbox=False)
    
            tweet["sentiment"] = res.result[0][0]['label']
            sent = tweet["sentiment"]
            sqs1.send_message(QueueUrl = 'https://sqs.us-west-2.amazonaws.com/435250124029/Queue2',MessageAttributes={
                    'Latitude': {
                'DataType': 'String',
                'StringValue': lat
    
            },
            'Longitude': {
                'DataType': 'String',
                'StringValue': lon
    
            },
            'Sentiment': {
                'DataType': 'String',
                'StringValue': sent
            },
            'Tweet_Text':{
            	'DataType':'String',
            	'StringValue': text
            },
            'Place':{
            	'DataType':'String',
            	'StringValue':place
            }
        }, MessageBody=json.dumps(tweet))
            #time.sleep(5)
            response = sns.publish(TargetArn=arn, Message = json.dumps(tweet), MessageAttributes = {})
            print(response)
            #print(tweet)
