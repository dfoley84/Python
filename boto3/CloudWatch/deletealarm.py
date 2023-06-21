import boto3 

Session = boto3.Session()
regions = ['eu-west-1', 'us-east-1', 'us-west-2', 'ap-southeast-2']

for region in regions:
    CW = Session.client(service_name='cloudwatch', region_name=region)

    response = CW.describe_alarms()
    filtered_alarms = [
        alarm for alarm in response['MetricAlarms']
        if alarm['MetricName'] == 'OldestMessage'
    ]
    for alarm in filtered_alarms:
        #Delete the alarm
        CW.delete_alarms(
            AlarmNames=[
                alarm['AlarmName']
            ]
        )
        print(f"Deleted: {alarm['AlarmName']}")
