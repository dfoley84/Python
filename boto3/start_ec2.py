import boto3

ec2_resource = boto3.resource('ec2')
ec2_client = boto3.client('ec2')

EC2_INSTANCE_ID = input('Enter the instance ID: ')
EC2Instance = ec2_resource.Instance(EC2_INSTANCE_ID)
EC2Instance.start()





