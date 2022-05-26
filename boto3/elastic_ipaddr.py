import boto3
import hvac

client = hvac.Client(url='http://VaultServer:8200')
read_response = client.read('secret/aws/credentials')

sec_key = read_response['data']['aws_secret_access_key']
acc_key = read_response['data']['aws_access_key_id']


session = boto3.Session(
    aws_access_key_id=acc_key,
    aws_secret_access_key=sec_key
    region_name='eu-west-1'
)

EC2_client = session.client('ec2')

response = EC2_client.describe_addresses()
for address in response['Addresses']:
    if address['InstanceId'] is None:
        EC2_client.release_address(AllocationId=address['AllocationId'])
