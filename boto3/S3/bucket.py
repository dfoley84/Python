import boto3
import json

class BucketPolicy:
    def __init__(self, bucket_name, bucket_policy):
        self.s3 = boto3.client('s3')
        self.bucket_name = bucket_name
        self.bucket_policy = bucket_policy

    def apply_policy(self):
        self.s3.put_bucket_policy(Bucket=self.bucket_name, Policy=json.dumps(self.bucket_policy))
        
    def block_public_access(self):
        self.s3.put_public_access_block(
        Bucket=self.bucket_name,
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': True,
            'IgnorePublicAcls': True,
            'BlockPublicPolicy': True,
            'RestrictPublicBuckets': True
        },
    )

def create_bucket(bucket_name, region):
    s3 = boto3.client('s3', region_name=region)
    try:
        s3.create_bucket(Bucket=bucket_name, 
                         CreateBucketConfiguration={'LocationConstraint': region})
        
        s3_waiter = s3.get_waiter('bucket_exists')
        s3_waiter.wait(Bucket=bucket_name)
        return True
    
    except Exception as e:
        print('Error: {}'.format(e))
        return False
