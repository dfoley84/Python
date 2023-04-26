from urllib import response
import boto3
from botocore.exceptions import ClientError

Session = boto3.Session()
s3 = boto3.client('s3', region_name='eu-west-1')

#Enable S3 Versioning
response = s3.list_buckets()
for bucket in response['Buckets']:
    try:
        s3.put_bucket_versioning(
            Bucket=bucket['Name'],
            VersioningConfiguration={
                'Status': 'Enabled'
            }
        )
    except ClientError as e:
        print("Bucket: %s, unexpected error: %s" % (bucket['Name'], e))
