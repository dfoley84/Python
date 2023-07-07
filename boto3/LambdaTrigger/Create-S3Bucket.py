import json
import boto3
import urllib3
from botocore.exceptions import ClientError

class BucketReplicationDelete:
    def __init__(self, s3, BucketName):
        self.s3 = s3
        self.BucketName = BucketName

    def BucketSearch(self):
        try:
            self.s3.head_bucket(Bucket=self.BucketName)
        except ClientError as e:
            if e.response['Error']['Code'] == "NoSuchBucket":
                print("Bucket does not exist:", self.BucketName)
            else:
                raise e
        else:
            return True
        return False
    
    def BucketDelete(self):
        if self.BucketSearch():
            self.s3.delete_bucket(Bucket=self.BucketName)
        else:
            print("Bucket does not exist:", self.BucketName)



def cloudformationresponse(event, context, response_status, response_data):
    response_body = json.dumps({
        "Status": response_status,
        "Reason": "See the details in CloudWatch Log Stream: " + context.log_stream_name,
        "PhysicalResourceId": context.log_stream_name,
        "StackId": event['StackId'],
        "RequestId": event['RequestId'],
        "LogicalResourceId": event['LogicalResourceId'],
        "Data": response_data
    })

    http = urllib3.PoolManager()
    try:
        response = http.request(
            method='PUT',
            url=event['ResponseURL'],
            body=response_body.encode('utf-8'),
            headers={
                'Content-Type': '',
                'Content-Length': str(len(response_body))
            }
        )
        print("Status code:", response.status)
    except Exception as e:
        print("Failed to send CloudFormation response:", e)



def lambda_handler(event, context):
    responseData = {}
    responseStatus = 'SUCCESS'
    print("REQUEST RECEIVED:\n" + json.dumps(event))

    try:
        requestType = event['RequestType']
        bucketName = event['ResourceProperties']['BucketName']
        destinationBucket = event['ResourceProperties'].get('DestinationBucket')
        Region = event['ResourceProperties']['Region']
        RoleARN = event['ResourceProperties']['RoleArn']
        AccountID = event['ResourceProperties']['AccountId']
        BucketARN = 'arn:aws:s3:::' + bucketName

        BucketDeletion = BucketReplicationDelete(s3, bucketName) 
        s3 = boto3.client('s3', region_name=Region)

        if requestType == 'Delete':
            BucketDeletion.BucketDelete()
        elif requestType == 'Update':
            pass
        elif requestType == 'Create':
            s3.create_bucket(
                Bucket=bucketName,
                CreateBucketConfiguration={
                    'LocationConstraint': Region
                }
            )

            s3.put_bucket_versioning(
                Bucket=bucketName,
                VersioningConfiguration={
                    'Status': 'Enabled'
                }
            )

            s3.put_bucket_replication(
                Bucket=bucketName,
                ReplicationConfiguration={
                    'Role': RoleARN,
                    'Rules': [
                        {
                            'ID': 'Bi-Directional',
                            'Status': 'Enabled',
                            'Prefix': '',
                            'Destination': {
                                'Bucket': 'arn:aws:s3:::' + destinationBucket
                            }
                        }
                    ]
                }
            )

            policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "1",
                        "Effect": "Allow",
                        "Principal": {
                            "AWS": RoleARN
                        },
                        "Action": [
                            "s3:ReplicateObject",
                            "s3:ReplicateDelete",
                        ],
                        "Resource": [
                            BucketARN+"/*"
                        ]
                    },
                    {
                        "Sid": "2",
                        "Effect": "Allow",
                        "Principal": {
                            "AWS": "arn:aws:iam::" + AccountID + ":root"
                        },
                        "Action": [
                            "s3:ObjectOwnerOverrideToBucketOwner"
                        ],
                        "Resource": [
                            BucketARN+"/*"
                        ]
                    },
                    {
                        "Sid": "3",
                        "Effect": "Allow",
                        "Principal": {
                            "AWS": RoleARN
                        },
                        "Action": [
                            "s3:GetBucketVersioning",
                            "s3:PutBucketVersioning"
                        ],
                        "Resource": [
                            BucketARN
                        ]
                    }
                ]
            }

            s3.put_bucket_policy(
                Bucket=bucketName,
                Policy=json.dumps(policy)
            )
    except Exception as e:
        print("Failed to process:", e)
        responseStatus = 'FAILED'
        if requestType == 'Create':
            BucketDeletion.BucketDelete()
    finally:
        cloudformationresponse(event, context, responseStatus, responseData)
