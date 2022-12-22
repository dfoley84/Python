#CIS 1.4: 3.9 Ensure VPC flow logging is enabled in all VPCs
import boto3 
from botocore.exceptions import ClientError

session = boto3.Session()
regions = ['eu-west-1','us-east-1','us-west-2','ap-southeast-2']

for region in regions:
    session = boto3.Session(region_name=region)
    client = boto3.client('logs')
    ec2 =  boto3.client('ec2')

    try:
        response = client.create_log_group(logGroupName='Testflowlog')
    except ClientError as e:
        print(e)


    #List out VPCs
    response = ec2.describe_vpcs()
    VPC_ID = response['Vpcs'][0]['VpcId']

    #Create Flow Log
    try:
        response = ec2.create_flow_logs(
            ResourceIds=[
                VPC_ID,
            ],
            ResourceType='VPC',
            TrafficType='ALL',
            LogGroupName='Testflowlog',
            DeliverLogsPermissionArn='arn:aws:iam:::role/'
        )
    except ClientError as e:
        print(e)
        continue

