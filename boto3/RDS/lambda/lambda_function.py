from urllib import response
import boto3
from botocore.exceptions import ClientError

from CreateSnapshot import snapshot
from CreateKMS import create_kms_key
from CopySnapshot import copy_snapshot
from ShareSnapshot import share_snapshot
from CopySnapshotDestination import CopySnapshotdown

if __name__ == "__main__":
    
    AWSRegion = input("Enter the AWS Region: ")
    RDSInstance = input("Enter the RDS Instance Name: ")
    AWSSourceAccountID = input("Enter Source AWS Account ID: ")
    AWSDestinationAccountID = input("Enter Destination AWS Account ID: ")

    sts_client = boto3.client('sts')
    response  = sts_client.assume_role(
        RoleArn="arn:aws:iam:::role/",
        RoleSessionName="Customer_Backup"
    )

    ACCESS_KEY = response['Credentials']['AccessKeyId']
    SECRET_KEY = response['Credentials']['SecretAccessKey']
    SESSION_TOKEN = response['Credentials']['SessionToken']

    #Calling the Functions
    snapshot(ACCESS_KEY,SECRET_KEY,SESSION_TOKEN,AWSRegion,RDSInstance)
    create_kms_key(ACCESS_KEY,SECRET_KEY,SESSION_TOKEN,AWSRegion,RDSInstance)
    copy_snapshot(ACCESS_KEY,SECRET_KEY,SESSION_TOKEN,AWSRegion,RDSInstance)
    share_snapshot(ACCESS_KEY,SECRET_KEY,SESSION_TOKEN,AWSRegion,RDSInstance,AWSDestinationAccountID)
    CopySnapshotdown(AWSRegion,RDSInstance,AWSSourceAccountID)
