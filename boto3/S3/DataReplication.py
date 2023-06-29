import boto3 
from botocore.exceptions import ClientError
import time

Buckets = []
assumed_role_object = None

try:
    Session = boto3.Session()
    sts_client = boto3.client('sts')
    assumed_role_object=sts_client.assume_role(
        RoleArn="<ROLE>",
        RoleSessionName="S3BackupAccount"
    )
except Exception as e:
    print(f"Error Assuming Role: {str(e)}")

if assumed_role_object:    
    ACCESS_KEY = assumed_role_object['Credentials']['AccessKeyId']
    SECRET_KEY = assumed_role_object['Credentials']['SecretAccessKey']
    SESSION_TOKEN = assumed_role_object['Credentials']['SessionToken']

    try:
        S3Source = boto3.client('s3')
        S3Backup = boto3.client('s3', 
                                    aws_access_key_id=ACCESS_KEY, 
                                    aws_secret_access_key=SECRET_KEY, 
                                    aws_session_token=SESSION_TOKEN)
        
        #List out all buckets in the source account with prefix '<>' and check if Replication is enabled
        response = S3Source.list_buckets()
        for bucket in response['Buckets']:
            if bucket['Name'].startswith('<BUCKET_PREFIX>'):
                try:
                    DataReplication = S3Source.get_bucket_replication(Bucket=bucket['Name'])
                    if DataReplication['ReplicationConfiguration']['Rules'][0]['Status'] == 'Enabled':
                        print(f"Bucket: {bucket['Name']} is already replicated")
                except ClientError as e:
                    error_code = e.response['Error']['Code']
                    # If Replication isn't enabled it will throw an Error, Catching Error, and then add the Bucket Name to list
                    if error_code == 'ReplicationConfigurationNotFoundError': 
                        print(f"Bucket: {bucket['Name']} is not replicated")
                        Buckets.append(bucket['Name'])
                    else:
                        print(f"Error: {str(e)}")
                 

        for bucket in Buckets:
            # Create Bucket in Backup Account and Enable Versioning
            S3Backup.create_bucket(Bucket='{}-backup'.format(bucket))
            S3Backup.put_bucket_versioning(
                Bucket='{}-backup'.format(bucket),
                VersioningConfiguration={ 'Status': 'Enabled' }
            )
            
            # Check if Bucket Versioning is enabled on source bucket
            versioning = S3Source.get_bucket_versioning(Bucket=bucket)
            if 'Status' not in versioning or versioning['Status'] != 'Enabled':
                S3Source.put_bucket_versioning(
                    Bucket=bucket,
                    VersioningConfiguration={
                        'Status': 'Enabled'
                    }
                )
                # Add delay to make sure the versioning configuration takes effect
                time.sleep(5)

            # Setup Data Replication Rule
            S3Source.put_bucket_replication(
                Bucket=bucket,
                ReplicationConfiguration={
                    'Role': '<ROLE>',
                    'Rules': [
                        {
                            'ID': '{}-backup'.format(bucket),
                            'Status': 'Enabled',
                            'Priority': 0,
                            'DeleteMarkerReplication': { 'Status': 'Disabled' },
                            'Filter': { 'Prefix': '' },
                            'Destination': {
                                'Bucket': 'arn:aws:s3:::{}-backup'.format(bucket),
                                'StorageClass': 'STANDARD'
                            }
                        }
                    ]
                }
            )
    except Exception as e:
        print(f"Error: {str(e)}")
