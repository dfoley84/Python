from urllib import response
import boto3
from botocore.exceptions import ClientError


def CopySnapshotdown(AWSRegion, RDSInstance, AWSSourceAccountID):
    session = boto3.Session()
    client = session.client('rds', region_name=AWSRegion)
    #Copy Share Snapshot to UAT Account
    response = client.copy_db_snapshot(
        SourceDBSnapshotIdentifier='arn:aws:rds:%s:%s:snapshot:%s-snapshot-shared' % (AWSRegion, AWSSourceAccountID, RDSInstance),
        TargetDBSnapshotIdentifier='%s-uat-snapshot' % RDSInstance,
        KmsKeyId='alias/aws/rds',
        CopyTags=False
    )
    waiter = client.get_waiter('db_snapshot_completed')
    waiter.wait(
        DBSnapshotIdentifier='%s-uat-snapshot',
        WaiterConfig={
                'Delay': 60,
                'MaxAttempts': 100
            }
        )
    print('Snapshot Completed', '\n')
        