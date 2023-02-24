from urllib import response
import boto3
from botocore.exceptions import ClientError


def snapshot(ACCESS_KEY,SECRET_KEY,SESSION_TOKEN,AWSRegion,RDSInstance):
    rds = boto3.client(
        'rds',
        region_name=AWSRegion,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN
    )

    try:
        response = rds.create_db_snapshot(
            DBInstanceIdentifier='%s' % RDSInstance,
            DBSnapshotIdentifier='%s-snapshot' % RDSInstance,
        )
        print('Creating Snapshot', '\n')
        waiter = rds.get_waiter('db_snapshot_completed')
        waiter.wait(
            DBSnapshotIdentifier='%s-snapshot' % RDSInstance,
            WaiterConfig={
                    'Delay': 60,
                    'MaxAttempts': 100
                }
            )
        print('Snapshot Completed', '\n')
    except ClientError as e:
        print(e)
