import boto3
from datetime import datetime, timedelta

class AMIChecker:
    def __init__(self, image_id, ec2_client):
        self.ec2_client = ec2_client
        self.image_id = image_id
    def check_ami_usage(self):
        Environment = self.ec2_client.describe_instances(
            Filters=[{'Name': 'image-id', 'Values': [self.image_id]}]
        )
        if not Environment['Reservations']:
            return None
        
        
