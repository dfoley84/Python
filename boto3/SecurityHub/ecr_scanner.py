from urllib import response
import boto3
from botocore.exceptions import ClientError
Session = boto3.Session()
regions = ['eu-west-1','us-east-1','us-west-2','ap-southeast-2']

for region in regions:
    ecr = boto3.client('ecr', region_name=region)
    #list all repositories
    try:
        response = ecr.describe_repositories()
        for repo in response['repositories']:
            RepoName = repo['repositoryName']
            try:
                response = ecr.put_image_scanning_configuration(
                    repositoryName=RepoName,
                    imageScanningConfiguration={
                        'scanOnPush': True
                    }
                )
                print(response)
            except ClientError as e:
                print(e)
    except ClientError as e:
        print(e)




