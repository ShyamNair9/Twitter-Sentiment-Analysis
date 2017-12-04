# TwitterTrendMap
### Sentiment Analysis of real-time Tweets 
using AWS SQS, SNS, Lambda functions and Elastic Search and S3 client.

This project is aimed at analyzing sentiments of tweets on Twitter, wherein a keyword is selected via a drop down on the User Interface and pinned on the world map.

This project is designed using JavaScript, Amazon Web Services and Python

![Alt text](Architecture.png?raw=true "Landing")

## Functionality

### Lambda function for fetching tweets
We use an SQS Queue to fetch real-time tweets using Twitter Streaming API via a Lambda function, upon confirming geolocation info and language is English. The lambda function receives a ping request from CloudWatch at a fixed interval to update the SQS Queue

### Lambda function to fetch tweets from SQS and trigger SNS
On selecting a keyword through the front-end UI dropdown, a request is sent to the API Gateway which triggers a 2nd AWS Lambda function and carries out the functionality of filtering the tweets with given keyword from the already generated SQS Queue and performs a sentiment analysis using the MonkeyLearn API. Once the sentiment is analyzed, a new tweet is formed and inserted into a new SQS queue. Following this the SNS notification response is prepared which acts as a trigger for the next Lambda function.

### Lambda function to submit tweets onto ElasticSearch
The second SQS queue acts as a buffer between the Lambda functions to fetch tweets from SQS to trigger SNS and Lambda function to submit refined tweets with sentiments to ElasticSearch, as the third Lambda function(triggered via the SNS) fetches tweets from the second SQS Queue and is then indexed in Amazon's Elastic Search.

### Pinning on the map
Once on ElasticSearch, the new tweets become available to iterate over via the front-end UI and are pinned on the world map using Google Maps API. On clicking, user can view the tweet, country and sentiment. 

The tweets have been flagged using customer markers  
RED for negative, YELLOW for neutral and GREEN for positive.

![Alt text](SentimentAnalysis.png?raw=true "Landing")

### Notifications
The front-end polls the back end ElasticSearch at reguar intervals in the background for the same keyword requested from the user and compares the count of tweets generated globally during the execution versus the fresh count, incase of new tweets, user receives a notification as below

![Alt text](Notification.png?raw=true "Landing")

#### The final website is hosted on Amazon's S3 Client on this link 
#### https://s3-us-west-2.amazonaws.com/twittersentiments/index.html


