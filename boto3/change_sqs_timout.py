import boto3 

regions = ['eu-west-1','ap-southeast-2','us-east-1','us-west-2']
session = boto3.Session()

for region in regions:
    sqs = session.client('sqs', region_name=region)
    response = sqs.list_queues()
    try:
        for queue in response['QueueUrls']:
            sqsgetattibute = sqs.get_queue_attributes(
            QueueUrl=queue, 
            AttributeNames=[
                'VisibilityTimeout'
            ])
            if sqsgetattibute['Attributes']['VisibilityTimeout'] == '30':
                changeTimout = sqs.set_queue_attributes(
                    QueueUrl=queue,
                    Attributes={
                        'VisibilityTimeout': '300'    
                    })
                print(queue)
    except Exception as e:
        print('Issue with: ' + queue)
        continue

                
