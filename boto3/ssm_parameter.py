import boto3
from operator import itemgetter

session = boto3.Session()
regions = []


ec2 = session.client('ec2',region_name='')
response = ec2.describe_images(Owners=["self"],
                                Filters=[{'Name':'name',
                                'Values':['ecs-hvm-2.0*']}])

image_details = sorted(response['Images'], key=itemgetter('CreationDate'), reverse=True)
ami_id = image_details[0]['ImageId']

for region in regions:
    ssm = session.client("ssm", region_name=region)
    response = ssm.put_parameter(
        Name="ecs-ami",
        Type="String",
        Overwrite=True,
        Value=ami_id)
print("AMI ID: " + ami_id)

