import json
import boto3
import urllib2
print('Loading function')
#i = 5
def lambda_handler(event, context):
    tweet_location = ""
    message = ''
    tweet_sentiment = ""
    try:
        message = ""
        client = boto3.client('sqs',aws_access_key_id='',aws_secret_access_key='',region_name='')
        queue_url = "https://sqs.us-west-2.amazonaws.com/435250124029/Queue2"
        response = client.receive_message(QueueUrl=queue_url,AttributeNames=['SentTimestamp'],MaxNumberOfMessages=10,MessageAttributeNames=['All'],VisibilityTimeout=0,WaitTimeSeconds=0)
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']
        client.delete_message(QueueUrl=queue_url,ReceiptHandle=receipt_handle)
        tweet_sentiment=message['MessageAttributes']['Sentiment']['StringValue']
        latitude=message['MessageAttributes']['Latitude']['StringValue']
        longitude=message['MessageAttributes']['Longitude']['StringValue']
        tweet_place = message['MessageAttributes']['Place']['StringValue']
        tweet_text = message['MessageAttributes']['Tweet_Text']['StringValue']
        data="{\"Latitude\":\""+latitude+"\",\"Longitude\":\""+longitude+"\",\"Sentiment\":\""+tweet_sentiment+"\",\"Place\":\""+tweet_place+"\",\"Tweet\":\""+tweet_text+"\"}"
        print(data)
        req=urllib2.urlopen("https://search-tweettrends-quwhy4tzdisvz7vd5e2qhq5o5i.us-west-2.es.amazonaws.com/final/shyam", data=data)
    except Exception as e:
        message=e.message
            
    return {
        'statusCode': 200,
        'headers': { 'Content-Type': 'application/json' ,
            'Access-Control-Allow-Origin' : '*'
        },
        'body': json.dumps({ 'username':  tweet_sentiment, 'id': 20 }
        )
            }
