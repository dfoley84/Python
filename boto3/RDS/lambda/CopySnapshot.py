from urllib import response
import boto3
from botocore.exceptions import ClientError

def copy_snapshot(ACCESS_KEY,SECRET_KEY,SESSION_TOKEN,AWSRegion,RDSInstance):
    print('Copying Snapshot', '\n')

    rds = boto3.client(
        'rds',
        region_name=AWSRegion,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN
    )
    try:
        response = rds.copy_db_snapshot(
            SourceDBSnapshotIdentifier='%s-snapshot' % RDSInstance,
            TargetDBSnapshotIdentifier='%s-snapshot-shared' % RDSInstance,
            KmsKeyId='alias/%s-snapshot' % RDSInstance,
            CopyTags=True,
            Tags=[
                {
                    'Key': '%s-snapshot' % RDSInstance,
                    'Value': '%s-snapshot' % RDSInstance
                },
            ]
        )
        print('Copying Snapshot', '\n')
        waiter = rds.get_waiter('db_snapshot_completed')
        waiter.wait(
            DBSnapshotIdentifier='%s-snapshot-shared' % RDSInstance,
            WaiterConfig={
                    'Delay': 60,
                    'MaxAttempts': 100
                }
            )
        print('Snapshot Completed', '\n')
    except ClientError as e:
        print(e)