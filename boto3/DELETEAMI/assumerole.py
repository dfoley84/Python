import boto3 


class AssumeRole:
    def __init__(self, role_arn, role_session_name):
        self.role_arn = role_arn
        self.role_session_name = role_session_name
        self.sts_client = boto3.client('sts')
        self.credentials = None
    
    def assume_role(self):
        self.credentials = self.sts_client.assume_role(
            RoleArn=self.role_arn,
            RoleSessionName=self.role_session_name
        )
        return self.credentials
        
