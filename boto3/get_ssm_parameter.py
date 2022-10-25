import boto3
import os 
import json

session = boto3.Session()
region = "eu-west-1"

ec2 = session.client('ssm', region_name=region)
response = ec2.get_parameter(
    Name='/aws/service/ecs/optimized-ami/amazon-linux-2/recommended')
Image_id = response['Parameter']['Value']
aList = json.loads(Image_id)
print(aList['image_id'])

#Get AMI ID and use as Linux Env variable for Codebuild.
#Image_id = $(python3 get_ssm_parameter.py)
#echo $Image_id
