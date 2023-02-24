from urllib import response
import boto3
from botocore.exceptions import ClientError


def snapshot_restore(AWSRegion, RDSInstance, DBSecurityGroup):
    session = boto3.Session()
    client = session.client('rds', region_name=AWSRegion)
    response = client.restore_db_instance_from_db_snapshot(
        DBInstanceIdentifier='%s-restore' % RDSInstance,
        DBSnapshotIdentifier='%s-uat-snapshot' % RDSInstance,
        DBInstanceClass='db.t2.micro',
        Port=3306,
        AvailabilityZone='%s-a' % AWSRegion,
        DBSubnetGroupName=DBSecurityGroup,
        MultiAZ=False,
        PubliclyAccessible=False,
        AutoMinorVersionUpgrade=False, 
        LicenseModel='general-public-license',
        Tags=[
            {
                'Key': '%s-restore' % RDSInstance,
                'Value': '%s-restore' % RDSInstance
            },
        ]
    )
    waiter = client.get_waiter('db_instance_available')
    waiter.wait(
        DBInstanceIdentifier='%s-restore' % RDSInstance,
        WaiterConfig={
                'Delay': 60,
                'MaxAttempts': 100
            }
        )
    print('Snapshot Restore Completed', '\n')

