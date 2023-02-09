from urllib import response
import boto3, json
from botocore.exceptions import ClientError

Session = boto3.Session()
#List out Default Security Groups
ec2 = boto3.client('ec2', region_name='ap-southeast-2')
response = ec2.describe_security_groups()
for sg in response['SecurityGroups']:
    if sg['GroupName'] == 'default':
      #Delete Outbound Rules
        for rule in sg['IpPermissionsEgress']:
            try:
                print('Deleting Outbound Rule: %s' % rule)
                ec2.revoke_security_group_egress(
                    GroupId = sg['GroupId'],
                    IpPermissions = [rule]
                )
            except ClientError as e:
                print("Unexpected error: %s" % e)
        #Delete Inbound Rules
        for rule in sg['IpPermissions']:
            try:
                print('Deleting Inbound Rule: %s' % rule)
                ec2.revoke_security_group_ingress(
                    GroupId = sg['GroupId'],
                    IpPermissions = [rule]
                )
            except ClientError as e:
                print("Unexpected error: %s" % e)
