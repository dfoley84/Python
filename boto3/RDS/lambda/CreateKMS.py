from urllib import response
import boto3
from botocore.exceptions import ClientError
import json


policy = """
{
    "Id": "key-consolepolicy-3",
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Enable IAM User Permissions",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam:::root"
            },
            "Action": "kms:*",
            "Resource": "*"
        },
        {
            "Sid": "Allow use of the key",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam:::root"
            },
            "Action": [
                "kms:Encrypt",
                "kms:Decrypt",
                "kms:ReEncrypt*",
                "kms:GenerateDataKey*",
                "kms:DescribeKey"
            ],
            "Resource": "*"
        },
        {
            "Sid": "Allow attachment of persistent resources",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam:::root"
            },
            "Action": [
                "kms:CreateGrant",
                "kms:ListGrants",
                "kms:RevokeGrant"
            ],
            "Resource": "*",
            "Condition": {
                "Bool": {
                    "kms:GrantIsForAWSResource": "true"
                }
            }
        }
    ]
}"""

#Create KMS Key for Shared Snapshot
def create_kms_key(ACCESS_KEY,SECRET_KEY,SESSION_TOKEN,AWSRegion,RDSInstance):
    print('Creating KMS Key', '\n')

    kms = boto3.client(
        'kms',  
        region_name=AWSRegion,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN
    )
    try:
        response = kms.create_key(
            Description='KMS Key for Shared Snapshot %s' % RDSInstance,
            KeyUsage='ENCRYPT_DECRYPT',
            Origin='AWS_KMS',
            MultiRegion=False,
            BypassPolicyLockoutSafetyCheck=False,
            Tags=[
                {
                    'TagKey': '%s-snapshot' % RDSInstance,
                    'TagValue': '%s-snapshot' % RDSInstance
                },
            ]
        )
        kms.create_alias(
            AliasName='alias/%s-snapshot1' % RDSInstance,
            TargetKeyId=response['KeyMetadata']['KeyId']
        )

        kms.put_key_policy(
            KeyId=response['KeyMetadata']['KeyId'],
            Policy=policy,
            PolicyName='default'
        )
    except ClientError as e:
        print(e)