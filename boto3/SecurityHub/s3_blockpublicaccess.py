#CIS 2.1.5.1:  S3 Block Public Access setting should be enabled

from urllib import response
import boto3
from botocore.exceptions import ClientError

Session = boto3.Session()

s3 = boto3.client('s3', region_name='eu-west-1')
response = s3.list_buckets()



for bucket in response['Buckets']:
    try:
        s3.put_public_access_block(
                Bucket = bucket['Name'],
                PublicAccessBlockConfiguration={
                    'BlockPublicAcls': True,
                    'IgnorePublicAcls': True,
                    'BlockPublicPolicy': True,
                    'RestrictPublicBuckets': True
                }
            )
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
            print('Bucket: %s, no public access block' % (bucket['Name']))
            s3.put_public_access_block(
                Bucket = bucket['Name'],
                PublicAccessBlockConfiguration={
                    'BlockPublicAcls': True,
                    'IgnorePublicAcls': True,
                    'BlockPublicPolicy': True,
                    'RestrictPublicBuckets': True
                }
            )

