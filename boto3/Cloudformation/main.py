from bucket import BucketPolicy, create_bucket
from cloneTenant import CloneStack 
from newTenant import NewTenant

if __name__ == "__main__":
    BackupAccountBucketName = '' 
    BackupAccountRegion = ''
    BackupAccountID = ''


    SourceRegion = ''
    DestinationRegion = ''

    SourceStackName = ''
    DestinationStackName = ''

    CloudFormationRoleARN = 'arn:aws:iam::ACCOUNT_ID:role/ROLE'

    CreateBackupBucket = False
    CopyStack = False
    NewStack = False


    if CreateBackupBucket:
        if create_bucket(BackupAccountBucketName, BackupAccountRegion):
            print(f"Bucket '{BackupAccountBucketName}' created successfully!")
            bucket_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "ForceSSLOnlyAccess",
                        "Effect": "Deny",
                        "Principal": "*",
                        "Action": "s3:*",
                        "Resource": [
                            f"arn:aws:s3:::{BackupAccountBucketName}/*",
                            f"arn:aws:s3:::{BackupAccountBucketName}"
                        ],
                        "Condition": {
                            "Bool": {
                                "aws:SecureTransport": "false"
                            }
                        }
                    }
                ]
            }
            bucket_policy_manager = BucketPolicy(BackupAccountBucketName, bucket_policy)
            bucket_policy_manager.apply_policy()
            bucket_policy_manager.block_public_access()

            print(f"Applied bucket policy to '{BackupAccountBucketName}' successfully!")
        else:
            print("Bucket creation failed.")

        

    if CopyStack: 
        updated_params = {
            'S3BucketName': '',
            'NetworkStackName': '',
            'SqsQueueName': '.fifo',
            'DBPassword': '',
            'S3Replication': ''
            }
        
        clone_cloudformation = CloneStack(SourceRegion, DestinationRegion, SourceStackName, DestinationStackName, updated_parameters=updated_params) 
        clone_cloudformation.CloneCFStack()

    if NewStack:
        with open('cf.yaml', 'r') as f:
            Template = f.read()

        #RDS Configuration
        AllocatedStorage = '10'
        StorageType = 'gp2'
      


        #S3 Configuration
        S3BucketName = ''
        S3BucketReplicationName = ''
        

        #KMS Configuration
      

        #SQS   
      
        parameters =[
            {'ParameterKey': 'AllocatedStorage', 'ParameterValue': AllocatedStorage},
        ]

        new_cloudformation = NewTenant(SourceRegion, SourceStackName, Template, parameters)
        new_cloudformation.CreateNewTenant()



