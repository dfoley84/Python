import boto3
from datetime import datetime, timedelta

def process_queue_decorator(func):
    def wrapper(queue_url, i):
        queue_name = queue_url.split('/')[-1]
        #skip dead letter queues
        if "SqsDeadLetterQueue" in queue_name:
            return
        print('Queue: {}'.format(queue_name))
        func(queue_name, i)
    return wrapper


@process_queue_decorator
def process_queue(queue_name, region):
    #Check if the SQS queue has any alarms set
    alarms = cw.describe_alarms_for_metric(
        MetricName='ApproximateAgeOfOldestMessage',
        Namespace='AWS/SQS',
        Dimensions=[
            {
                'Name': 'QueueName',
                'Value': queue_name
            },
        ]
    )
    if alarms['MetricAlarms']:
        print('Alarm already exists for queue: {}'.format(queue_name))
    else:
        #Create an alarm for the queue
        print('Creating alarm for queue: {}'.format(queue_name))
        alarm_name = '{}-SQSAlarm'.format(queue_name)
        
        #Create an Alarm for ApproximateAgeOfOldestMessage
        response = cw.put_metric_alarm(
            AlarmName=alarm_name,
            ComparisonOperator='GreaterThanThreshold',
            EvaluationPeriods=2,
            MetricName='ApproximateAgeOfOldestMessage',
            Namespace='AWS/SQS',
            Period=3600,
            Statistic='Maximum',
            Threshold=600,
            TreatMissingData = 'missing',
            ActionsEnabled=True,
            OKActions=[
                'arn:aws:sns:{}::sqs-alerts'.format(region)
            ],
            AlarmActions=[
                'arn:aws:sns:{}::sqs-alerts'.format(region)
            ],
            AlarmDescription='{} ApproximateAgeOfOldestMessage Alarm'.format(queue_name),
            Dimensions=[
                {
                    'Name': 'QueueName',
                    'Value': queue_name
                },
            ],
            Unit='Seconds'
        )

region = [
    'eu-west-1',
    'us-east-1',
    'us-west-2',
    'ap-southeast-2'
]


for i in region:
    sqs = boto3.client('sqs', region_name=i)
    cw = boto3.client('cloudwatch', region_name=i)

    #List out all queues expect dead letter queues
    response = sqs.list_queues()
    queue_urls = response.get('QueueUrls', [])

    # Process each queue
    for queue_url in queue_urls:
        process_queue(queue_url, i)
