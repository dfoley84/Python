from datetime import datetime, timedelta
import boto3
import json 
import os
import boto3.session
from assumerole import AssumeRole
from Checkami import AMIChecker

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super(DateTimeEncoder, self).default(o)

region = ['eu-west-1', 'us-west-2', 'us-east-1', 'ap-southeast-2']
def lambda_handler(event, context):
    for i in region:
        ec2 = boto3.client('ec2', region_name=i)
        prod_arn = os.environ['production_arn']
        sandbox_arn = os.environ['sandbox_arn']
       
        production_role = AssumeRole(prod_arn, 'RoleSessionName')
        prod_credentials = production_role.assume_role()['Credentials']
        prod_ec2 = boto3.client('ec2', region_name=i,
                                    aws_access_key_id=prod_credentials['AccessKeyId'],
                                    aws_secret_access_key=prod_credentials['SecretAccessKey'],
                                    aws_session_token=prod_credentials['SessionToken']
                                )
        sandbox_role = AssumeRole(sandbox_arn, 'RoleSessionName')
        sandbox_credentials = sandbox_role.assume_role()['Credentials']
        sandbox_ec2 = boto3.client('ec2', region_name=i,
                                    aws_access_key_id=sandbox_credentials['AccessKeyId'],
                                    aws_secret_access_key=sandbox_credentials['SecretAccessKey'],
                                    aws_session_token=sandbox_credentials['SessionToken']
                                )
        try:
            ec2AMIImage = ec2.describe_images(
                Owners=['self']
            )
        except Exception as e:
            raise e 
        
        for Image in ec2AMIImage['Images']:
            if os.environ['IMAGENAME'] in Image['Name']:
                if Image['CreationDate'] < (datetime.now() - timedelta(days=90)).isoformat():
                    try:
                        uat_ami = ec2.describe_instances(
                            Filters=[
                                {   
                                    'Name': 'image-id',
                                    'Values': [Image['ImageId']]
                                }
                            ]
                        )
                        if not uat_ami['Reservations']: 
                            try:
                                sandboxchekcer = AMIChecker(Image['ImageId'], sandbox_ec2).check_ami_usage()
                                productionchekcer = AMIChecker(Image['ImageId'], prod_ec2).check_ami_usage()
                                if not sandboxchekcer and not productionchekcer:
                                    print(f"Region: {i} \n Image Name: {Image['Name']} \n AMI: {Image['ImageId']} is not in use in any environment")
                                    #Derigister the AMI within UAT
                                    try:
                                        reponse = ec2.deregister_image(
                                            ImageId=Image['ImageId']
                                        )
                                        print(f"Region {i} \n Image Name: {Image['Name']} \n AMI: {Image['ImageId']} has been deregistered")
                                    except Exception as e:
                                        raise e
                            except Exception as e:
                                raise e
                    except Exception as e:
                        raise e
