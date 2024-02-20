import boto3 
from datetime import datetime, timedelta


nowtime = datetime.now()
start_time = nowtime - timedelta(hours = 48)
start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')

now_str = nowtime.strftime('%Y-%m-%dT%H:%M:%SZ')

session = boto3.Session()



def get_zero_connections(region):
    client = session.client('rds',region_name=region)
    cloudwatch = boto3.client('cloudwatch',region_name=region)
    zero_connections = []
    response = client.describe_db_instances()
    for rds in response['DBInstances']:
        isinstance = rds['DBInstanceIdentifier']

        #Get Monitoring Data for the Instance reference https://gist.github.com/xpepper/c1a87d2e3ce855815286281432eff7e0
        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/RDS',
            MetricName='DatabaseConnections',
            Dimensions=[
                {
                    'Name': 'DBInstanceIdentifier',
                    'Value': isinstance
                },
            ],
            StartTime=start_time_str,
            EndTime=now_str,
            Period=3600,
             Statistics=[
                'Average',
            ],
        )
        if not response['Datapoints'] or response['Datapoints'][-1]['Average'] == 0:
            print(f"RDS instance {isinstance} has zero connections.")
          #Removed appending to List.
    return zero_connections
        
if __name__ == '__main__':
    region = ['eu-west-1', 'us-east-1', 'us-west-2', 'ap-southeast-2' ]
    for i in region:
        get_zero_connections(i)

