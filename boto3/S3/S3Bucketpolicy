from urllib import response
import boto3
from botocore.exceptions import ClientError

Session = boto3.Session()
s3 = boto3.client('s3', region_name='eu-west-1')
response = s3.list_buckets()

for bucket in response['Buckets']:
    #block public access
    try:
        bpa = s3.get_public_access_block(Bucket = bucket['Name'])
        print('Bucket: %s, BlockPublicAccess: %s' % (bucket['Name'], bpa))
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
            print('Bucket: %s, no block public access' % (bucket['Name']))
            s3.put_public_access_block(
                Bucket = bucket['Name'],
                PublicAccessBlockConfiguration={
                    'BlockPublicAcls': True,
                    'IgnorePublicAcls': True,
                    'BlockPublicPolicy': True,
                    'RestrictPublicBuckets': True
                }
            )
        else:
            print("Bucket: %s, unexpected error: %s" % (bucket['Name'], e))
