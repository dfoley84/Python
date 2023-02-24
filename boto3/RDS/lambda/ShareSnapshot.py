from urllib import response
import boto3
from botocore.exceptions import ClientError
import json

def share_snapshot(ACCESS_KEY,SECRET_KEY,SESSION_TOKEN,AWSRegion,RDSInstance,AWSDestinationAccountID):
    print('Sharing Snapshot', '\n')

    rds = boto3.client(
        'rds',
        region_name=AWSRegion,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN
    )
    try:
        response = rds.modify_db_snapshot_attribute(
            DBSnapshotIdentifier='%s-snapshot-shared' % RDSInstance,
            AttributeName='restore',
            ValuesToAdd=[
                '%s' % AWSDestinationAccountID,
            ]
        )
    except ClientError as e:
        print(e)