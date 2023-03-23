from urllib import response
import boto3, json
from botocore.exceptions import ClientError

Session = boto3.Session()
region = ['eu-west-1', 'us-east-1', 'us-west-2', 'ap-southeast-2']

for i in region:
    sns = boto3.client('sns', region_name=i)
    Lambda = boto3.client('lambda', region_name=i)
    topics = sns.list_topics()

    for topic_arn in topics['Topics']:
        topic_attributes = sns.get_topic_attributes(TopicArn=topic_arn['TopicArn'])
        if topic_attributes['Attributes'].get('KmsMasterKeyId'):
            subscriptions = sns.list_subscriptions_by_topic(TopicArn=topic_arn['TopicArn'])
            for subscription in subscriptions['Subscriptions']:
                if subscription['Protocol'] == 'lambda':
                    Lambda.get_function(FunctionName=subscription['Endpoint'])
                    print(f"Found SNS Topic {topic_arn['TopicArn']} with KMS Key {topic_attributes['Attributes']['KmsMasterKeyId']} and Lambda Subscription {subscription['Endpoint']}")
