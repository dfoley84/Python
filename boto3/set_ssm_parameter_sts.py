import boto3
from boto3.session import Session
from operator import itemgetter

# Create a session
session = boto3.Session()

#Assume Role
role_info = {
    'RoleArn': 'arn:aws:iam::<AWS Account>:role/<RoleName>',
    'RoleSessionName': '<Role Name>'
    }
client = boto3.client('sts')
credentials = client.assume_role(**role_info)
session2 = boto3.session.Session(
    aws_access_key_id=credentials['Credentials']['AccessKeyId'],
    aws_secret_access_key=credentials['Credentials']['SecretAccessKey'],
    aws_session_token=credentials['Credentials']['SessionToken']
    )

UserRoles = [session, session2]

regions = ["eu-west-1", "us-east-1", "us-west-2", "ap-southeast-2"]
for region in regions:
    ec2 = session.client('ec2', region_name=region)

    response = ec2.describe_images(Owners=["self"],
                                Filters=[{'Name':'name',
                                'Values':['<Image Name>-*']}])

    image_details = sorted(response['Images'], key=itemgetter('CreationDate'), reverse=True)
    ami_id = image_details[0]['ImageId']

    for i in UserRoles:
        ssm = i.client("ssm", region_name=region)
        response = ssm.put_parameter(
            Name="packer-ecs-ami",
            Type="String",
            Overwrite=True,
            Value=ami_id)
        print("AMI ID: " + ami_id)

