from urllib import response
import boto3, json
from botocore.exceptions import ClientError

Session = boto3.Session()
s3 = boto3.client('s3', region_name='eu-west-1')
response = s3.list_buckets()

for bucket in response['Buckets']:
    #Create a policy if it doesn't exist
    try:
        policy = s3.get_bucket_policy(Bucket = bucket['Name'])
        print('Bucket: %s, Policy: %s' % (bucket['Name'], policy))
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
            print('Bucket: %s, no bucket policy' % (bucket['Name']))
            s3.put_bucket_policy(
                Bucket = bucket['Name'],
                Policy = json.dumps({
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Sid": "AllowSSLRequestsOnly",
                            "Effect": "Deny",
                            "Principal": "*",
                            "Action": "s3:*",
                            "Resource": [
                                "arn:aws:s3:::%s/*" % bucket['Name'],
                                "arn:aws:s3:::%s" % bucket['Name']
                            ],
                            "Condition": {
                                "Bool": {
                                    "aws:SecureTransport": "false"
                                }
                            }
                        }
                    ]
                })
            )
        else:
            print("Bucket: %s, unexpected error: %s" % (bucket['Name'], e))
