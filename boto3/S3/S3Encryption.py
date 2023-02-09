from urllib import response
import boto3
from botocore.exceptions import ClientError

Session = boto3.Session()
s3 = boto3.client('s3', region_name='eu-west-1')
response = s3.list_buckets()

for bucket in response['Buckets']:
    try:
        enc = s3.get_bucket_encryption(Bucket = bucket['Name'])
        rules = enc['ServerSideEncryptionConfiguration']['Rules']
        print('Bucket: %s, Encryption: %s' % (bucket['Name'], rules))
    except ClientError as e:
        if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
            print('Bucket: %s, no server-side encryption' % (bucket['Name']))
            s3.put_bucket_encryption(
                Bucket = bucket['Name'],
                 ServerSideEncryptionConfiguration={
                    "Rules": [
                        {"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}
                        ]
                    },
                )
        else:
            print("Bucket: %s, unexpected error: %s" % (bucket['Name'], e))
