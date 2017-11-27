# TwitterTrendMap
### Sentiment Analysis of real-time Tweets 
using AWS SQS, SNS, Lambda functions and Elastic Search and S3 client.

This project is aimed at analyzing sentiments of tweets on Twitter, wherein a keyword is selected via a drop down on the User Interface and pinned on the world map.

This project is designed using JavaScript, Amazon Web Services, Python.

## Functionality

### Fetching tweets
We use an SQS Queue to fetch real-time tweets using Twitter Streaming API upon confirming geolocation info and language is English.

### Lambda function to fetch tweets from SQS and trigger SNS
On selecting a keyword through the front-end UI dropdown, an AWS Lambda function is triggered, which carries out the functionality of filtering the tweets with given keyword from the already generated SQS Queue and performs a sentiment analysis using the MonkeyLearn API. Once the sentiment is analyzed, a new tweet is formed and inserted into a new SQS queue. Following this the SNS notification response is prepared which acts as a trigger for the next Lambda function.

### Lambda function to submit tweets onto ElasticSearch
The second SQS queue acts as a buffer between the two Lambda functions, as the second Lambda function(triggered via the SNS) fetches tweets from the second SQS Queue and is then indexed in Amazon's Elastic Search.

### Pinning on the map
Once on ElasticSearch, the new tweets become available to iterate over via the front-end UI and are pinned on the world map using Google Maps API. On clicking, user can view the tweet, country and sentiment. 

The tweets have been flagged using customer markers  
RED for negative, YELLOW for neutral and GREEN for positive.

![Alt text](SentimentAnalysis.png?raw=true "Landing")

### Notifications
The front-end polls the back end ElasticSearch at reguar intervals and compares the count of tweets generated globally during the execution versus the fresh count, incase of new tweets, user receives a notification.

#### The final website is hosted on Amazon's S3 Client.


