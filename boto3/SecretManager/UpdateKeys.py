import boto3

session = boto3.session.Session()
secrets_manager = session.client('secretsmanager', region_name='eu-west-1')
key_alias = 'alias/aws/secretsmanager'


paginator = secrets_manager.get_paginator('list_secrets')
key_arns = []

for page in paginator.paginate():
    key_arns.extend(page['SecretList'])
    
    for secret in key_arns:
        secret_metadata = secrets_manager.describe_secret(SecretId=secret['ARN'])
        update_key = False

        if 'KmsKeyId' in secret_metadata:
            kms_key_id = secret_metadata['KmsKeyId']
            if kms_key_id != key_alias:
                update_key = True
                break
      
    if update_key:
        secrets_manager.update_secret(SecretId=secret['ARN'], KmsKeyId=key_alias)
        print(f"Secret {secret['ARN']} updated")

